from datetime import date

from django.db import migrations, models


def seed_blog(apps, schema_editor):
    BlogSection = apps.get_model("main", "BlogSection")
    BlogPost = apps.get_model("main", "BlogPost")

    BlogSection.objects.get_or_create(
        pk=1,
        defaults={
            "badge_text": "ПОЛЕЗНО ЗНАТЬ",
            "title_prefix": "Статьи",
            "title_highlight": "и советы",
            "description": (
                "Полезные материалы о шлифовке, отделке и уходе за деревянным домом — "
                "от специалистов ArteMadera."
            ),
            "archive_url": "https://artemadera.ru/blog/",
            "archive_link_text": "Все статьи блога",
            "is_visible": True,
        },
    )

    posts = [
        {
            "title": "Можно ли шлифовать сруб зимой?",
            "excerpt": (
                "Как создают тепловой контур на объекте и почему профессиональная шлифовка "
                "возможна не только в тёплый сезон."
            ),
            "url": "https://artemadera.ru/blog/",
            "static_image": "images/portfolio-2.jpg",
            "published_at": date(2025, 1, 15),
            "sort_order": 0,
        },
        {
            "title": 'Что такое «тёплый шов» для деревянного дома',
            "excerpt": (
                "Зачем нужен эластичный герметик в межвенцовых швах и как он защищает "
                "древесину от влаги и продуваний."
            ),
            "url": "https://artemadera.ru/blog/",
            "static_image": "images/service-1.jpg",
            "published_at": date(2024, 11, 8),
            "sort_order": 1,
        },
        {
            "title": "Как подготовить дом из бруса к покраске",
            "excerpt": (
                "Этапы шлифовки, удаления пыли и выбора системы покрытия для долговечной "
                "защиты фасада."
            ),
            "url": "https://artemadera.ru/blog/",
            "static_image": "images/service-2.jpg",
            "published_at": date(2024, 9, 22),
            "sort_order": 2,
        },
    ]
    for post in posts:
        BlogPost.objects.get_or_create(
            title=post["title"],
            defaults={**post, "is_active": True},
        )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0008_portfolio_cases"),
    ]

    operations = [
        migrations.CreateModel(
            name="BlogSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("badge_text", models.CharField(default="ПОЛЕЗНО ЗНАТЬ", max_length=64, verbose_name="Бейдж")),
                ("title_prefix", models.CharField(default="Статьи", max_length=80, verbose_name="Заголовок (белая часть)")),
                ("title_highlight", models.CharField(default="и советы", max_length=80, verbose_name="Заголовок (акцент)")),
                ("description", models.TextField(default="Полезные материалы о шлифовке, отделке и уходе за деревянным домом — от специалистов ArteMadera.", verbose_name="Описание")),
                ("archive_url", models.URLField(default="https://artemadera.ru/blog/", verbose_name="Ссылка «Все статьи»")),
                ("archive_link_text", models.CharField(default="Все статьи блога", max_length=80, verbose_name="Текст ссылки на блог")),
                ("is_visible", models.BooleanField(default=True, verbose_name="Показывать блок")),
            ],
            options={"verbose_name": "Блок «Блог»", "verbose_name_plural": "Блок «Блог»"},
        ),
        migrations.CreateModel(
            name="BlogPost",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200, verbose_name="Заголовок")),
                ("excerpt", models.TextField(verbose_name="Краткое описание")),
                ("url", models.URLField(help_text="Полный URL на artemadera.ru или другую страницу", verbose_name="Ссылка на статью")),
                ("image", models.ImageField(blank=True, null=True, upload_to="blog/", verbose_name="Обложка (загрузка)")),
                ("static_image", models.CharField(blank=True, help_text="Например images/portfolio-1.jpg", max_length=200, verbose_name="Обложка (static)")),
                ("published_at", models.DateField(blank=True, null=True, verbose_name="Дата публикации")),
                ("sort_order", models.IntegerField(default=0, verbose_name="Порядок")),
                ("is_active", models.BooleanField(default=True, verbose_name="Показывать")),
            ],
            options={
                "verbose_name": "Статья блога",
                "verbose_name_plural": "Статьи блога",
                "ordering": ["sort_order", "-published_at", "pk"],
            },
        ),
        migrations.RunPython(seed_blog, migrations.RunPython.noop),
    ]
