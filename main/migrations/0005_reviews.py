from django.db import migrations, models


def seed_reviews(apps, schema_editor):
    ReviewsSection = apps.get_model("main", "ReviewsSection")
    Review = apps.get_model("main", "Review")

    ReviewsSection.objects.get_or_create(
        pk=1,
        defaults={
            "badge_text": "ОТЗЫВЫ",
            "title_prefix": "Что говорят",
            "title_highlight": "клиенты",
            "yandex_maps_url": "https://yandex.ru/maps/org/artemadera/45828270851/",
            "yandex_rating": 5.0,
            "is_visible": True,
        },
    )

    items = [
        (
            "Ольга Б.",
            "Финский стиль",
            "Ребята из «ArteMadera» отличаются редким качеством — умением слышать потребности заказчика "
            "и предлагать простые решения сложных задач. Только здесь поняли нашу идею строений в финском стиле, "
            "прониклись ею и выполнили очень сложную работу с отличным качеством.",
            0,
        ),
        (
            "Иваныч",
            "Рекомендую ArteMadera",
            "Рекомендую данную фирму. Ребята работают чётко, быстро, слаженно, а главное — честно и открыто.",
            1,
        ),
        (
            "Пётр",
            "Дом из бруса",
            "О компании узнали от знакомых. В 2020 году построили двухэтажный брусовой дом на сложных почвах — "
            "результатом остались довольны.",
            2,
        ),
        (
            "Александр К.",
            "Лучший менеджер",
            "Хочется отметить безупречное, добросовестное отношение к обязанностям менеджеров компании "
            "ArteMadera. Спасибо за сопровождение на всех этапах!",
            3,
        ),
        (
            "Константин",
            "Дом мечты",
            "Дом собрали очень качественно и быстро. Получилось именно то, что хотели. "
            "Спасибо большое за проделанную работу!",
            4,
        ),
        (
            "Татьяна",
            "Остались довольны",
            "Замечательная фирма, строят уже не первый год. Я довольна сотрудничеством с ними.",
            5,
        ),
    ]
    for author, headline, text, order in items:
        Review.objects.get_or_create(
            author_name=author,
            headline=headline,
            defaults={
                "text": text,
                "rating": 5,
                "source": "yandex",
                "sort_order": order,
                "is_active": True,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0004_experience"),
    ]

    operations = [
        migrations.CreateModel(
            name="ReviewsSection",
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
                    models.CharField(default="ОТЗЫВЫ", max_length=64, verbose_name="Бейдж"),
                ),
                (
                    "title_prefix",
                    models.CharField(
                        default="Что говорят",
                        max_length=64,
                        verbose_name="Заголовок (белая часть)",
                    ),
                ),
                (
                    "title_highlight",
                    models.CharField(
                        default="клиенты",
                        max_length=64,
                        verbose_name="Заголовок (акцент)",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        default=(
                            "Реальные отзывы с Яндекс.Карт и сайта ArteMadera — о шлифовке, "
                            "отделке и работе команды на объекте."
                        ),
                        verbose_name="Описание",
                    ),
                ),
                (
                    "yandex_maps_url",
                    models.URLField(
                        default="https://yandex.ru/maps/org/artemadera/45828270851/",
                        verbose_name="Ссылка на Яндекс.Карты",
                    ),
                ),
                (
                    "yandex_rating",
                    models.DecimalField(
                        decimal_places=1,
                        default=5.0,
                        max_digits=2,
                        verbose_name="Рейтинг (для отображения)",
                    ),
                ),
                (
                    "yandex_reviews_count",
                    models.PositiveIntegerField(
                        blank=True,
                        default=0,
                        verbose_name="Кол-во отзывов (0 — не показывать)",
                    ),
                ),
                (
                    "is_visible",
                    models.BooleanField(default=True, verbose_name="Показывать блок"),
                ),
            ],
            options={
                "verbose_name": "Блок «Отзывы»",
                "verbose_name_plural": "Блок «Отзывы»",
            },
        ),
        migrations.CreateModel(
            name="Review",
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
                    "author_name",
                    models.CharField(max_length=120, verbose_name="Имя автора"),
                ),
                (
                    "headline",
                    models.CharField(max_length=200, verbose_name="Заголовок отзыва"),
                ),
                ("text", models.TextField(verbose_name="Текст отзыва")),
                (
                    "rating",
                    models.PositiveSmallIntegerField(default=5, verbose_name="Оценка (1–5)"),
                ),
                (
                    "source",
                    models.CharField(
                        choices=[
                            ("yandex", "Яндекс.Карты"),
                            ("site", "Сайт"),
                        ],
                        default="yandex",
                        max_length=16,
                        verbose_name="Источник",
                    ),
                ),
                ("sort_order", models.IntegerField(default=0, verbose_name="Порядок")),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Показывать"),
                ),
            ],
            options={
                "verbose_name": "Отзыв",
                "verbose_name_plural": "Отзывы",
                "ordering": ["sort_order", "pk"],
            },
        ),
        migrations.RunPython(seed_reviews, migrations.RunPython.noop),
    ]
