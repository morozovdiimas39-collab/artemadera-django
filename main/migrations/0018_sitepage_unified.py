from django.db import migrations, models
import django.db.models.deletion

PAGE_SEEDS = [
    (0, "home", "Главная", True),
    (10, "shlifovka", "Шлифовка", False),
    (20, "pokraska", "Покраска", False),
    (30, "teplyy-shov", "Тёплый шов", False),
    (40, "obsada", "Обсада / окосячка", False),
    (41, "obsada/okna", "Обсада окон", False),
    (42, "obsada/dveri", "Обсада дверей", False),
    (50, "injeneriya", "Инженерия", False),
    (60, "kryshi", "Крыши", False),
    (70, "otdelka/konopatka", "Конопатка", False),
    (71, "otdelka/sten", "Отделка стен", False),
    (72, "otdelka/pola", "Отделка пола", False),
    (80, "otdelka/shlifovka/sruba", "Шлифовка срубов", False),
    (81, "otdelka/shlifovka/ocilindrovannogo-brevna", "Шлифовка оцил. бревна", False),
    (82, "otdelka/shlifovka/brusa", "Шлифовка бруса", False),
    (83, "otdelka/shlifovka/lafeta", "Шлифовка лафета", False),
    (90, "proizvodstvo/besedki", "Беседки", False),
    (91, "proizvodstvo/falshbalki", "Фальшбалки", False),
    (92, "proizvodstvo/plintusy", "Плинтусы", False),
]


def migrate_to_sitepage(apps, schema_editor):
    SitePage = apps.get_model("main", "SitePage")
    PageServiceLink = apps.get_model("main", "PageServiceLink")
    Service = apps.get_model("main", "Service")
    PageHero = apps.get_model("main", "PageHero")

    hero_by_key = {}
    for hero in PageHero.objects.all():
        hero_by_key[hero.page_key] = hero

    home_page = None
    for sort_order, page_key, title, show_services in PAGE_SEEDS:
        hero = hero_by_key.get(page_key)
        defaults = {
            "title": title,
            "sort_order": sort_order,
            "show_services_block": show_services,
            "is_active": True,
            "hero_static_image": "images/hero-bg.jpg",
        }
        if hero:
            defaults["hero_static_image"] = hero.hero_static_image or "images/hero-bg.jpg"
            if hero.title:
                defaults["title"] = hero.title
        if page_key == "home":
            defaults["services_badge"] = "Наши услуги"
            defaults["services_title_white"] = "Отделка "
            defaults["services_title_accent"] = "деревянных домов"
            defaults["services_lead"] = (
                "Основные направления ArteMadera — от подготовки древесины до кровли и инженерии."
            )
            defaults["hero_h1_white"] = "Отделка"
            defaults["hero_h1_accent"] = "деревянных домов"
            defaults["hero_lead"] = (
                "Шлифовка, покраска, обсада и комплексные работы под ключ.\n"
                "Гарантия на работы, фиксированная смета, бесплатный выезд замерщика."
            )

        page, _ = SitePage.objects.update_or_create(page_key=page_key, defaults=defaults)
        if hero and hero.hero_image:
            page.hero_image = hero.hero_image
            page.save(update_fields=["hero_image"])
        if page_key == "home":
            home_page = page

    if home_page:
        order = 0
        for svc in Service.objects.filter(show_on_homepage=True).order_by("order", "pk"):
            PageServiceLink.objects.get_or_create(
                page=home_page,
                service=svc,
                defaults={
                    "sort_order": order,
                    "layout": svc.home_layout or "",
                    "tag_override": svc.home_tag_override or "",
                    "is_visible": True,
                },
            )
            order += 1


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0017_pagehero"),
    ]

    operations = [
        migrations.CreateModel(
            name="SitePage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "page_key",
                    models.CharField(
                        help_text="Без начального слэша: home — главная, obsada/okna — /obsada/okna",
                        max_length=160,
                        unique=True,
                        verbose_name="URL страницы",
                    ),
                ),
                ("title", models.CharField(max_length=120, verbose_name="Название в админке")),
                ("is_active", models.BooleanField(default=True, verbose_name="Активна")),
                ("sort_order", models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")),
                (
                    "hero_image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="pages/hero/",
                        verbose_name="Фон первого экрана",
                    ),
                ),
                (
                    "hero_static_image",
                    models.CharField(
                        blank=True,
                        default="images/hero-bg.jpg",
                        help_text="Если нет загрузки, например images/hero-bg.jpg",
                        max_length=200,
                        verbose_name="Фон (static)",
                    ),
                ),
                (
                    "hero_h1_white",
                    models.CharField(blank=True, max_length=200, verbose_name="Заголовок H1 (белая часть)"),
                ),
                (
                    "hero_h1_accent",
                    models.CharField(
                        blank=True,
                        help_text="Можно перенос строки — отобразится как <br>",
                        max_length=200,
                        verbose_name="Заголовок H1 (акцент)",
                    ),
                ),
                ("hero_lead", models.TextField(blank=True, verbose_name="Подзаголовок под H1")),
                (
                    "show_services_block",
                    models.BooleanField(default=False, verbose_name="Показывать блок услуг"),
                ),
                (
                    "services_badge",
                    models.CharField(
                        blank=True,
                        default="Наши услуги",
                        max_length=64,
                        verbose_name="Бейдж блока услуг",
                    ),
                ),
                (
                    "services_title_white",
                    models.CharField(blank=True, max_length=120, verbose_name="Заголовок услуг (белый)"),
                ),
                (
                    "services_title_accent",
                    models.CharField(blank=True, max_length=120, verbose_name="Заголовок услуг (акцент)"),
                ),
                ("services_lead", models.TextField(blank=True, verbose_name="Текст под заголовком услуг")),
            ],
            options={
                "verbose_name": "Страница",
                "verbose_name_plural": "Страницы",
                "ordering": ("sort_order", "title"),
            },
        ),
        migrations.CreateModel(
            name="PageServiceLink",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("sort_order", models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")),
                (
                    "layout",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("", "Обычная"),
                            ("wide", "Широкая (2 колонки)"),
                            ("last", "Широкая в конце сетки"),
                        ],
                        default="",
                        max_length=16,
                        verbose_name="Раскладка карточки",
                    ),
                ),
                (
                    "tag_override",
                    models.CharField(
                        blank=True,
                        help_text="Пусто — из калькулятора услуги.",
                        max_length=64,
                        verbose_name="Бейдж (вручную)",
                    ),
                ),
                ("is_visible", models.BooleanField(default=True, verbose_name="Показывать")),
                (
                    "page",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="service_links",
                        to="main.sitepage",
                        verbose_name="Страница",
                    ),
                ),
                (
                    "service",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="page_links",
                        to="main.service",
                        verbose_name="Услуга",
                    ),
                ),
            ],
            options={
                "verbose_name": "Услуга на странице",
                "verbose_name_plural": "Услуги на странице",
                "ordering": ("sort_order", "pk"),
                "unique_together": {("page", "service")},
            },
        ),
        migrations.RunPython(migrate_to_sitepage, noop),
        migrations.DeleteModel(
            name="PageHero",
        ),
    ]
