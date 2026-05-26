from types import SimpleNamespace

from django.db.utils import OperationalError

from .models import PageServiceLink, SitePage

DEFAULT_STATIC_HERO = "images/hero-bg.jpg"


def normalize_page_key(path: str) -> str:
    key = (path or "/").strip("/")
    return key or "home"


def default_site_page(page_key: str):
    return SimpleNamespace(
        page_key=page_key,
        title="",
        hero_image=None,
        has_hero_upload=False,
        hero_static_image=DEFAULT_STATIC_HERO,
        hero_h1_white="",
        hero_h1_accent="",
        hero_lead="",
        show_services_block=False,
        services_badge="",
        services_title_white="",
        services_title_accent="",
        services_lead="",
        is_active=True,
        service_links=[],
    )


def get_site_page(request):
    page_key = normalize_page_key(request.path)
    try:
        page = (
            SitePage.objects.filter(page_key=page_key, is_active=True)
            .prefetch_related("service_links__service__calculator_profile")
            .first()
        )
        if page:
            return page
    except OperationalError:
        pass
    return default_site_page(page_key)


def _title_segments(title: str) -> tuple[str, str]:
    """«Обсада / окосячка» → («Обсада», «окосячка»)."""
    t = (title or "").strip()
    if " / " in t:
        head, tail = t.split(" / ", 1)
        return head.strip(), tail.strip()
    return t, ""


def services_block_captions(page) -> dict[str, str]:
    """
    Подписи блока услуг: явные поля из админки, иначе — из названия страницы (title),
    чтобы не показывать дефолт «Наши услуги» на каждом разделе.
    """
    badge = (getattr(page, "services_badge", None) or "").strip()
    tw = (getattr(page, "services_title_white", None) or "").strip()
    ta = (getattr(page, "services_title_accent", None) or "").strip()
    title = (getattr(page, "title", None) or "").strip()

    if tw or ta:
        head, _tail = _title_segments(title)
        return {
            "badge": badge or head or title or "Услуги",
            "title_white": tw,
            "title_accent": ta,
        }

    head, tail = _title_segments(title)
    if head and tail:
        return {
            "badge": badge or head,
            "title_white": head,
            "title_accent": tail,
        }
    if head:
        return {
            "badge": badge or head,
            "title_white": head,
            "title_accent": "",
        }
    return {
        "badge": badge or "Услуги",
        "title_white": "Наши ",
        "title_accent": "услуги",
    }


def get_page_service_cards(page_key: str):
    """Карточки услуг для страницы (главная и др.)."""
    try:
        links = (
            PageServiceLink.objects.filter(
                page__page_key=page_key,
                page__is_active=True,
                is_visible=True,
                service__is_active=True,
            )
            .select_related("service", "service__calculator_profile", "page")
            .order_by("sort_order", "pk")
        )
        return [_ServiceCard(link) for link in links]
    except OperationalError:
        return []


class _ServiceCard:
    """Обёртка для шаблона: данные услуги + настройки размещения на странице."""

    def __init__(self, link: PageServiceLink):
        self._link = link
        self._service = link.service

    @property
    def name(self):
        return self._service.name

    @property
    def short_description(self):
        return self._service.short_description

    @property
    def image(self):
        return self._service.image

    @property
    def static_image(self):
        return self._service.static_image

    @property
    def link_url(self):
        return self._service.link_url

    @property
    def home_layout(self):
        return self._link.layout or self._service.home_layout

    def get_home_tag(self):
        return self._link.get_tag()

    @property
    def cta_label(self):
        return (getattr(self._link, "cta_label", None) or "").strip()


def get_shlifovka_page_service_cards():
    """Только строки «Услуги на странице» для страницы shlifovka (админка → Страницы → Шлифовка)."""
    return get_page_service_cards("shlifovka")
