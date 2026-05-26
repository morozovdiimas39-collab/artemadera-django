from django.db import migrations, models


PAGE_HEROES = [
    (0, "home", "Главная"),
    (10, "shlifovka", "Шлифовка"),
    (20, "pokraska", "Покраска"),
    (30, "teplyy-shov", "Тёплый шов"),
    (40, "obsada", "Обсада / окосячка"),
    (41, "obsada/okna", "Обсада окон"),
    (42, "obsada/dveri", "Обсада дверей"),
    (50, "injeneriya", "Инженерия"),
    (60, "kryshi", "Крыши"),
    (70, "otdelka/konopatka", "Конопатка"),
    (71, "otdelka/sten", "Отделка стен"),
    (72, "otdelka/pola", "Отделка пола"),
    (80, "otdelka/shlifovka/sruba", "Шлифовка срубов"),
    (81, "otdelka/shlifovka/ocilindrovannogo-brevna", "Шлифовка оцилиндрованного бревна"),
    (82, "otdelka/shlifovka/brusa", "Шлифовка бруса"),
    (83, "otdelka/shlifovka/lafeta", "Шлифовка лафета"),
    (90, "proizvodstvo/besedki", "Беседки"),
    (91, "proizvodstvo/falshbalki", "Фальшбалки"),
    (92, "proizvodstvo/plintusy", "Плинтусы"),
]


def seed_page_heroes(apps, schema_editor):
    PageHero = apps.get_model("main", "PageHero")
    for sort_order, page_key, title in PAGE_HEROES:
        PageHero.objects.get_or_create(
            page_key=page_key,
            defaults={
                "title": title,
                "sort_order": sort_order,
                "hero_static_image": "images/hero-bg.jpg",
                "is_active": True,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0016_service_homepage"),
    ]

    operations = [
        migrations.CreateModel(
            name="PageHero",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "page_key",
                    models.CharField(
                        help_text="URL без ведущего слэша: home — главная, obsada/okna — /obsada/okna",
                        max_length=160,
                        unique=True,
                        verbose_name="Ключ страницы",
                    ),
                ),
                ("title", models.CharField(max_length=120, verbose_name="Название в админке")),
                (
                    "hero_image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="page_heroes/",
                        verbose_name="Фоновое изображение",
                    ),
                ),
                (
                    "hero_static_image",
                    models.CharField(
                        blank=True,
                        default="images/hero-bg.jpg",
                        help_text="Путь относительно static/, например images/hero-bg.jpg",
                        max_length=200,
                        verbose_name="Статичный файл (если нет загрузки)",
                    ),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="Активно")),
                (
                    "sort_order",
                    models.PositiveSmallIntegerField(default=0, verbose_name="Порядок"),
                ),
            ],
            options={
                "verbose_name": "Фон hero страницы",
                "verbose_name_plural": "Фоны hero страниц",
                "ordering": ("sort_order", "title"),
            },
        ),
        migrations.RunPython(seed_page_heroes, migrations.RunPython.noop),
    ]
