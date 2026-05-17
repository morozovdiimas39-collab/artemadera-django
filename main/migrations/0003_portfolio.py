from django.db import migrations, models


def seed_portfolio(apps, schema_editor):
    PortfolioSection = apps.get_model("main", "PortfolioSection")
    PortfolioProject = apps.get_model("main", "PortfolioProject")

    PortfolioSection.objects.get_or_create(
        pk=1,
        defaults={
            "badge_text": "ПОРТФОЛИО",
            "title_prefix": "Наши",
            "title_highlight": "проекты",
            "description": (
                "Оцените качество нашей работы: мы бережно восстанавливаем древесину, "
                "возвращая домам первозданный вид и надёжную защиту."
            ),
            "is_visible": True,
        },
    )

    defaults = [
        ("images/service-1.jpg", "Деревянный дом", 0),
        ("images/portfolio-1.jpg", "Шлифовка сруба", 1),
        ("images/portfolio-2.jpg", "Работа на объекте", 2),
        ("images/service-2.jpg", "Интерьер из бруса", 3),
        ("images/service-3.jpg", "Шлифовка бревна", 4),
        ("images/portfolio-3.jpg", "Готовый результат", 5),
    ]
    for static_path, alt, order in defaults:
        PortfolioProject.objects.get_or_create(
            static_image=static_path,
            defaults={
                "alt_text": alt,
                "sort_order": order,
                "is_active": True,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_calculator"),
    ]

    operations = [
        migrations.CreateModel(
            name="PortfolioSection",
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
                    "badge_text",
                    models.CharField(
                        default="ПОРТФОЛИО", max_length=64, verbose_name="Бейдж"
                    ),
                ),
                (
                    "title_prefix",
                    models.CharField(
                        default="Наши", max_length=64, verbose_name="Заголовок (белая часть)"
                    ),
                ),
                (
                    "title_highlight",
                    models.CharField(
                        default="проекты",
                        max_length=64,
                        verbose_name="Заголовок (акцент)",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        default=(
                            "Оцените качество нашей работы: мы бережно восстанавливаем древесину, "
                            "возвращая домам первозданный вид и надёжную защиту."
                        ),
                        verbose_name="Описание",
                    ),
                ),
                (
                    "is_visible",
                    models.BooleanField(default=True, verbose_name="Показывать блок"),
                ),
            ],
            options={
                "verbose_name": "Блок «Наши проекты»",
                "verbose_name_plural": "Блок «Наши проекты»",
            },
        ),
        migrations.CreateModel(
            name="PortfolioProject",
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
                    "title",
                    models.CharField(blank=True, max_length=200, verbose_name="Подпись"),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="portfolio/",
                        verbose_name="Фото (загрузка)",
                    ),
                ),
                (
                    "static_image",
                    models.CharField(
                        blank=True,
                        help_text="Если файл не загружен: images/portfolio-1.jpg",
                        max_length=200,
                        verbose_name="Фото из static",
                    ),
                ),
                (
                    "alt_text",
                    models.CharField(blank=True, max_length=255, verbose_name="Alt-текст"),
                ),
                ("sort_order", models.IntegerField(default=0, verbose_name="Порядок")),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Показывать"),
                ),
            ],
            options={
                "verbose_name": "Проект портфолио",
                "verbose_name_plural": "Проекты портфолио",
                "ordering": ["sort_order", "pk"],
            },
        ),
        migrations.RunPython(seed_portfolio, migrations.RunPython.noop),
    ]
