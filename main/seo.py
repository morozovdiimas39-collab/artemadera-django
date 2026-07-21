from __future__ import annotations

import json
from dataclasses import dataclass

from django.conf import settings
from django.templatetags.static import static


CANONICAL_HOST = "artemadera.ru"
SITE_URL = f"https://{CANONICAL_HOST}"
COMPANY_NAME = "ArteMadera"
PHONE = "+7 (495) 005-01-45"
ADDRESS = "Ярославская ул., д. 8, корп. 6, офис 220"


@dataclass(frozen=True)
class SeoDefault:
    title: str
    description: str
    service_name: str = ""
    image: str = "images/hero-bg.jpg"


SEO_DEFAULTS: dict[str, SeoDefault] = {
    "home": SeoDefault(
        "Отделка деревянного дома в Москве и МО | ArteMadera",
        "Комплексная отделка деревянного дома в Москве и Московской области: шлифовка, покраска, тёплый шов, обсада, кровля и инженерия под ключ.",
        "Отделка деревянного дома",
        "images/hero-bg.jpg",
    ),
    "shlifovka": SeoDefault(
        "Шлифовка деревянного дома в Москве и МО | цена за м²",
        "Профессиональная шлифовка деревянных домов, срубов, бруса, лафета и ОЦБ в Москве и Московской области. Бесплатный замер, смета и гарантия.",
        "Шлифовка деревянного дома",
        "images/service-1.jpg",
    ),
    "pokraska": SeoDefault(
        "Покраска деревянного дома в Москве и МО | цена за м²",
        "Покраска деревянных домов снаружи и внутри в Москве и МО: срубы, брус, лафет и ОЦБ. Подбор ЛКМ, выкрасы, фиксированная смета.",
        "Покраска деревянного дома",
        "images/quiz/quiz_pokraska_1776809864700.png",
    ),
    "teplyy-shov": SeoDefault(
        "Тёплый шов для деревянного дома в Москве и МО | герметизация",
        "Герметизация межвенцовых швов деревянного дома в Москве и Московской области. Тёплый шов для сруба, бруса и ОЦБ без продуваний.",
        "Тёплый шов для деревянного дома",
        "services/teplyy-shov-finished.webp",
    ),
    "obsada": SeoDefault(
        "Обсада окон и дверей в деревянном доме в Москве и МО",
        "Изготовление и монтаж обсады оконных и дверных проёмов в деревянных домах. Компенсация усадки, подготовка под окна и двери.",
        "Обсада в деревянном доме",
        "images/quiz/quiz_brus_1776809793588.png",
    ),
    "obsada/okna": SeoDefault(
        "Обсада окон в деревянном доме в Москве и МО",
        "Обсадные короба для окон в деревянном доме: подготовка проёмов, защита от усадки, монтаж под любые размеры окон.",
        "Обсада окон",
        "images/quiz/quiz_brus_1776809793588.png",
    ),
    "obsada/dveri": SeoDefault(
        "Обсада дверей в деревянном доме в Москве и МО",
        "Обсада дверных проёмов в деревянном доме: входные и межкомнатные двери, компенсационный зазор и аккуратный монтаж.",
        "Обсада дверей",
        "images/quiz/quiz_brus_1776809793588.png",
    ),
    "otdelochnye-raboty": SeoDefault(
        "Отделочные работы в деревянном доме в Москве и МО | под ключ",
        "Внутренняя и внешняя отделка деревянного дома под ключ: стены, полы, проёмы, погонаж, шлифовка и подготовка к покраске.",
        "Отделочные работы в деревянном доме",
        "images/service-2.jpg",
    ),
    "otdelka/sten": SeoDefault(
        "Отделка стен в деревянном доме в Москве и МО",
        "Отделка стен деревянного дома: подготовка поверхности, монтаж погонажных изделий, декоративная отделка и защита древесины.",
        "Отделка стен деревянного дома",
        "images/service-2.jpg",
    ),
    "otdelka/pola": SeoDefault(
        "Отделка пола в деревянном доме в Москве и МО",
        "Отделка деревянных полов: подготовка основания, шлифовка, монтаж и финишная обработка покрытий в деревянном доме.",
        "Отделка пола в деревянном доме",
        "images/service-2.jpg",
    ),
    "otdelka/konopatka": SeoDefault(
        "Конопатка деревянного дома в Москве и МО",
        "Конопатка сруба и деревянного дома: утепление межвенцовых швов, устранение продуваний и подготовка к дальнейшей отделке.",
        "Конопатка деревянного дома",
        "images/before-after/before-1.png",
    ),
    "otdelka/shlifovka/sruba": SeoDefault(
        "Шлифовка сруба в Москве и МО | подготовка под покраску",
        "Шлифовка срубов из бревна: удаление старого покрытия, выравнивание древесины и подготовка фасада под финишную защиту.",
        "Шлифовка сруба",
        "images/service-1.jpg",
    ),
    "otdelka/shlifovka/brusa": SeoDefault(
        "Шлифовка бруса в Москве и МО | клеёный и профилированный брус",
        "Шлифовка домов из профилированного и клеёного бруса без повреждения геометрии. Подготовка стен к покраске и защите.",
        "Шлифовка бруса",
        "images/service-2.jpg",
    ),
    "otdelka/shlifovka/ocilindrovannogo-brevna": SeoDefault(
        "Шлифовка оцилиндрованного бревна в Москве и МО",
        "Аккуратная шлифовка дома из оцилиндрованного бревна с сохранением профиля, фактуры древесины и подготовкой под ЛКМ.",
        "Шлифовка оцилиндрованного бревна",
        "images/portfolio-1.jpg",
    ),
    "otdelka/shlifovka/lafeta": SeoDefault(
        "Шлифовка лафета в Москве и МО | плоскогранный брус",
        "Шлифовка домов из лафета и плоскогранного бруса: ровная поверхность без сколов, подготовка к покраске и отделке.",
        "Шлифовка лафета",
        "images/portfolio-2.jpg",
    ),
    "otdelka/shlifovka/bani-i-sauny": SeoDefault(
        "Шлифовка бани и сауны в Москве и МО",
        "Шлифовка деревянных бань и саун с учётом влажности, температурных нагрузок и подготовки древесины к защитным составам.",
        "Шлифовка бани и сауны",
        "images/service-3.jpg",
    ),
    "otdelka/shlifovka/konsyerzhnaya": SeoDefault(
        "Финишная шлифовка деревянного дома в Москве и МО",
        "Тонкая финишная шлифовка деревянных стен перед покраской, маслом или декоративной отделкой для ровной поверхности.",
        "Финишная шлифовка деревянного дома",
        "images/service-3.jpg",
    ),
    "kryshi": SeoDefault(
        "Кровельные работы в деревянном доме в Москве и МО",
        "Монтаж и ремонт кровли деревянных домов: стропильные системы, утепление, водостоки и аккуратная работа с деревянными конструкциями.",
        "Кровельные работы",
        "images/portfolio-3.jpg",
    ),
    "injeneriya": SeoDefault(
        "Инженерные коммуникации в деревянном доме в Москве и МО",
        "Проектирование и монтаж инженерных коммуникаций в деревянных домах: электрика, отопление, водоснабжение, канализация и вентиляция.",
        "Инженерные коммуникации",
        "images/after.jpg",
    ),
    "proizvodstvo": SeoDefault(
        "Производство изделий из дерева на заказ в Москве и МО",
        "Собственное производство деревянных изделий под проект: погонаж, фальшбалки, плинтусы, беседки и элементы отделки.",
        "Производство изделий из дерева",
        "images/portfolio-1.jpg",
    ),
    "proizvodstvo/besedki": SeoDefault(
        "Производство деревянных беседок на заказ в Москве и МО",
        "Изготовление деревянных беседок под проект: подбор древесины, производство элементов и подготовка к сборке.",
        "Деревянные беседки на заказ",
        "images/portfolio-1.jpg",
    ),
    "proizvodstvo/falshbalki": SeoDefault(
        "Фальшбалки из дерева на заказ в Москве и МО",
        "Производство деревянных фальшбалок и декоративных элементов под размеры проекта для интерьеров деревянных домов.",
        "Фальшбалки из дерева",
        "images/portfolio-1.jpg",
    ),
    "proizvodstvo/plintusy": SeoDefault(
        "Деревянные плинтусы на заказ в Москве и МО",
        "Изготовление деревянных плинтусов и погонажных изделий под проект с обработкой древесины на собственном производстве.",
        "Деревянные плинтусы",
        "images/portfolio-1.jpg",
    ),
    "o-kompanii": SeoDefault(
        "О компании ArteMadera | отделка деревянных домов",
        "ArteMadera — строительно-отделочная компания полного цикла для деревянных домов: опыт более 10 лет, договор, гарантия и собственное производство.",
        "",
        "images/team.png",
    ),
    "stroitelstvo/karkasnye-doma": SeoDefault(
        "Строительство каркасных домов в Москве и МО | под ключ",
        "Строительство каркасных домов под ключ в Москве и Московской области: проект, комплектация, тёплый контур, инженерия и отделка у одного подрядчика.",
        "Строительство каркасных домов",
        "images/hero-bg.jpg",
    ),
}


def normalize_page_key(path: str) -> str:
    key = (path or "/").strip("/")
    return key or "home"


def canonical_path_for_key(page_key: str) -> str:
    if page_key == "home":
        return "/"
    return "/" + page_key.strip("/")


def absolute_url(path: str) -> str:
    if not path.startswith("/"):
        path = "/" + path
    return SITE_URL + path


def image_url(static_path: str = "") -> str:
    path = static_path or "images/hero-bg.jpg"
    return absolute_url(static(path))


def company_schema() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": COMPANY_NAME,
        "url": SITE_URL + "/",
        "telephone": PHONE,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": ADDRESS,
            "addressLocality": "Москва",
            "addressCountry": "RU",
        },
        "areaServed": ["Москва", "Московская область"],
    }


def breadcrumb_schema(page_key: str, title: str) -> dict:
    items = [
        {"@type": "ListItem", "position": 1, "name": "Главная", "item": SITE_URL + "/"}
    ]
    if page_key != "home":
        items.append(
            {
                "@type": "ListItem",
                "position": 2,
                "name": title,
                "item": absolute_url(canonical_path_for_key(page_key)),
            }
        )
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def service_schema(page_key: str, default: SeoDefault) -> dict | None:
    if not default.service_name:
        return None
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": default.service_name,
        "description": default.description,
        "url": absolute_url(canonical_path_for_key(page_key)),
        "areaServed": ["Москва", "Московская область"],
        "provider": company_schema(),
    }


def build_page_seo(request, page=None) -> dict:
    page_key = normalize_page_key(request.path)
    default = SEO_DEFAULTS.get(page_key) or SeoDefault(
        f"{getattr(page, 'title', '') or 'Услуги для деревянного дома'} | ArteMadera",
        "Профессиональные работы с деревянными домами в Москве и Московской области: отделка, защита древесины, гарантия и бесплатный замер.",
        getattr(page, "title", "") or "",
    )

    title = (getattr(page, "seo_title", "") or "").strip() or default.title
    description = (getattr(page, "seo_description", "") or "").strip() or default.description
    canonical_path = canonical_path_for_key(page_key)
    canonical_url = absolute_url(canonical_path)
    noindex = bool(getattr(page, "seo_noindex", False))
    image = image_url(default.image)

    schema_items = [company_schema(), breadcrumb_schema(page_key, title)]
    service = service_schema(page_key, default)
    if service:
        schema_items.append(service)

    return {
        "title": title,
        "description": description,
        "canonical_url": canonical_url,
        "noindex": noindex,
        "og_type": "website",
        "og_image": image,
        "schema_json": json.dumps(schema_items, ensure_ascii=False),
    }


def build_blog_list_seo() -> dict:
    schema = [
        company_schema(),
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Главная", "item": SITE_URL + "/"},
                {"@type": "ListItem", "position": 2, "name": "Блог", "item": SITE_URL + "/blog/"},
            ],
        },
    ]
    return {
        "title": "Блог ArteMadera | советы по отделке деревянных домов",
        "description": "Статьи ArteMadera о шлифовке, покраске, тёплом шве, обсаде и уходе за деревянным домом от специалистов по отделке.",
        "canonical_url": SITE_URL + "/blog/",
        "noindex": False,
        "og_type": "website",
        "og_image": image_url("images/hero-bg.jpg"),
        "schema_json": json.dumps(schema, ensure_ascii=False),
    }


def build_blog_post_seo(post) -> dict:
    title = f"{post.title} | ArteMadera"
    description = (post.excerpt or "").strip()[:220]
    if post.image:
        image = absolute_url(post.image.url)
    elif post.static_image:
        image = image_url(post.static_image)
    else:
        image = image_url("images/hero-bg.jpg")
    canonical_url = SITE_URL + post.get_absolute_url()
    schema = [
        company_schema(),
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": post.title,
            "description": description,
            "url": canonical_url,
            "datePublished": post.published_at.isoformat() if post.published_at else None,
            "image": image,
            "publisher": {"@type": "Organization", "name": COMPANY_NAME, "url": SITE_URL + "/"},
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Главная", "item": SITE_URL + "/"},
                {"@type": "ListItem", "position": 2, "name": "Блог", "item": SITE_URL + "/blog/"},
                {"@type": "ListItem", "position": 3, "name": post.title, "item": canonical_url},
            ],
        },
    ]
    schema = [{k: v for k, v in item.items() if v is not None} for item in schema]
    return {
        "title": title,
        "description": description,
        "canonical_url": canonical_url,
        "noindex": False,
        "og_type": "article",
        "og_image": image,
        "schema_json": json.dumps(schema, ensure_ascii=False),
    }


def sitemap_paths() -> set[str]:
    return {canonical_path_for_key(key) for key in SEO_DEFAULTS.keys()}
