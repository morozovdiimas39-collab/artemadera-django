from __future__ import annotations

from urllib.parse import urlencode

from django.conf import settings
from django.http import HttpResponsePermanentRedirect


class CanonicalHostMiddleware:
    """Сводит публичные URL к одной SEO-канонической версии."""

    CANONICAL_HOST = "artemadera.ru"
    TRAILING_SLASH_EXCLUDE_PREFIXES = (
        "/admin/",
        "/blog/",
        "/export/",
        "/lead-status/",
        settings.MEDIA_URL,
        settings.STATIC_URL,
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        redirect_url = self._canonical_url(request)
        if redirect_url:
            return HttpResponsePermanentRedirect(redirect_url)
        return self.get_response(request)

    def _canonical_url(self, request) -> str:
        host = request.get_host().split(":", 1)[0].lower()
        if host not in {"artemadera.ru", "www.artemadera.ru"}:
            return ""

        path = request.path or "/"
        canonical_path = path
        if (
            path != "/"
            and path.endswith("/")
            and not any(path.startswith(prefix) for prefix in self.TRAILING_SLASH_EXCLUDE_PREFIXES)
        ):
            canonical_path = path.rstrip("/")

        forwarded_proto = request.META.get("HTTP_X_FORWARDED_PROTO", "").split(",", 1)[0].strip()
        scheme_is_http = forwarded_proto == "http" or (
            not forwarded_proto
            and request.scheme == "http"
            and request.META.get("SERVER_PORT") == "80"
        )
        needs_redirect = host != self.CANONICAL_HOST or scheme_is_http or canonical_path != path
        if not needs_redirect:
            return ""

        query = request.META.get("QUERY_STRING", "")
        suffix = f"?{query}" if query else ""
        return f"https://{self.CANONICAL_HOST}{canonical_path}{suffix}"
