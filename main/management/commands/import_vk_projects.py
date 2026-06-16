import json
import os
import re
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from main.models import PortfolioProject, PortfolioProjectImage
from main.portfolio_utils import sync_portfolio_photo_order


VK_API_URL = "https://api.vk.com/method/"
VK_API_VERSION = "5.199"
USER_AGENT = "ArteMadera VK portfolio importer/1.0"


def clean_text(value):
    return re.sub(r"\s+", " ", (value or "").strip())


def project_title(text, post_id):
    first_line = next((line.strip() for line in (text or "").splitlines() if line.strip()), "")
    first_line = re.sub(r"https?://\S+", "", first_line).strip(" -—|")
    return (first_line[:200] or f"Проект из VK #{post_id}").strip()


def largest_photo_url(photo):
    sizes = photo.get("sizes") or []
    if not sizes:
        return ""
    best = max(sizes, key=lambda size: (size.get("width", 0) * size.get("height", 0)))
    return best.get("url", "")


class Command(BaseCommand):
    help = "Imports VK wall posts with photos into portfolio projects."

    def add_arguments(self, parser):
        parser.add_argument("--group", default="artemadera", help="VK group screen name.")
        parser.add_argument("--count", type=int, default=50, help="Number of recent wall posts to inspect.")
        parser.add_argument("--offset", type=int, default=0, help="Wall posts offset.")
        parser.add_argument(
            "--commit",
            action="store_true",
            help="Create projects and download photos. Without this flag, only previews changes.",
        )
        parser.add_argument(
            "--json",
            dest="json_path",
            help="Read a saved VK wall.get response from JSON instead of calling the VK API.",
        )

    def handle(self, *args, **options):
        if options["json_path"]:
            posts = self._posts_from_json(options["json_path"])
            group_name = options["group"]
        else:
            token = os.environ.get("VK_ACCESS_TOKEN", "").strip()
            if not token:
                raise CommandError(
                    "VK requires an access token. Set VK_ACCESS_TOKEN and run the command again."
                )
            group = self._api("groups.getById", token, group_id=options["group"])[0]
            group_name = group.get("screen_name") or options["group"]
            wall = self._api(
                "wall.get",
                token,
                owner_id=-int(group["id"]),
                count=max(1, min(options["count"], 100)),
                offset=max(0, options["offset"]),
            )
            posts = wall.get("items", [])

        candidates = [post for post in posts if self._post_photos(post)]
        self.stdout.write(
            f"Found {len(candidates)} posts with photos out of {len(posts)} inspected posts."
        )

        created = 0
        skipped = 0
        for post in candidates:
            source_url = f"https://vk.com/{group_name}?w=wall{post['owner_id']}_{post['id']}"
            title = project_title(post.get("text"), post["id"])
            photos = self._post_photos(post)
            existing = PortfolioProject.objects.filter(source_url=source_url).first()

            if existing:
                skipped += 1
                self.stdout.write(f"SKIP existing: {title} ({source_url})")
                continue

            self.stdout.write(f"{'IMPORT' if options['commit'] else 'WOULD IMPORT'}: {title}")
            self.stdout.write(f"  {len(photos)} photo(s), {source_url}")
            if not options["commit"]:
                continue

            self._create_project(post, title, source_url, photos)
            created += 1

        if options["commit"]:
            self.stdout.write(self.style.SUCCESS(f"Created {created}; skipped {skipped}."))
        else:
            self.stdout.write(
                self.style.WARNING("Dry run only. Add --commit after reviewing the list.")
            )

    def _api(self, method, token, **params):
        params.update(access_token=token, v=VK_API_VERSION)
        url = f"{VK_API_URL}{method}?{urlencode(params)}"
        try:
            with urlopen(Request(url, headers={"User-Agent": USER_AGENT}), timeout=30) as response:
                payload = json.load(response)
        except (HTTPError, URLError, TimeoutError) as exc:
            raise CommandError(f"VK API request failed: {exc}") from exc
        if "error" in payload:
            raise CommandError(f"VK API error: {payload['error'].get('error_msg', payload['error'])}")
        return payload["response"]

    def _posts_from_json(self, path):
        try:
            payload = json.loads(Path(path).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise CommandError(f"Could not read VK JSON: {exc}") from exc
        response = payload.get("response", payload)
        return response.get("items", response) if isinstance(response, dict) else response

    def _post_photos(self, post):
        photos = []
        for attachment in post.get("attachments") or []:
            if attachment.get("type") == "photo" and attachment.get("photo"):
                photo = attachment["photo"]
                if largest_photo_url(photo):
                    photos.append(photo)
        return photos

    @transaction.atomic
    def _create_project(self, post, title, source_url, photos):
        text = (post.get("text") or "").strip()
        project = PortfolioProject.objects.create(
            title=title,
            summary=clean_text(text)[:300],
            description=text,
            source_url=source_url,
            sort_order=PortfolioProject.objects.count(),
            is_active=True,
        )
        for index, photo in enumerate(photos):
            url = largest_photo_url(photo)
            image_bytes, extension = self._download(url)
            filename = f"vk_{post['owner_id']}_{post['id']}_{photo['id']}_{index}{extension}"
            item = PortfolioProjectImage(
                project=project,
                sort_order=index,
                is_cover=index == 0,
                is_active=True,
            )
            item.image.save(filename, ContentFile(image_bytes), save=True)
        sync_portfolio_photo_order(project)

    def _download(self, url):
        try:
            with urlopen(Request(url, headers={"User-Agent": USER_AGENT}), timeout=45) as response:
                content = response.read()
                content_type = response.headers.get_content_type()
        except (HTTPError, URLError, TimeoutError) as exc:
            raise CommandError(f"Could not download photo {url}: {exc}") from exc
        extension = {
            "image/jpeg": ".jpg",
            "image/png": ".png",
            "image/webp": ".webp",
        }.get(content_type)
        if not extension:
            extension = Path(urlparse(url).path).suffix.lower()
        if extension not in {".jpg", ".jpeg", ".png", ".webp"}:
            extension = ".jpg"
        return content, extension
