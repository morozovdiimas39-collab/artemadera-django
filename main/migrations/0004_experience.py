from django.db import migrations, models


def seed_experience(apps, schema_editor):
    ExperienceSection = apps.get_model("main", "ExperienceSection")
    ExperienceStat = apps.get_model("main", "ExperienceStat")
    ExperienceAdvantage = apps.get_model("main", "ExperienceAdvantage")

    ExperienceSection.objects.get_or_create(pk=1)

    stats = [
        ("10+", "Лет на рынке", 0),
        ("500+", "Выполненных объектов", 1),
        ("1", "Подрядчик на весь цикл", 2),
        ("3 года", "Гарантия на работы", 3),
    ]
    for value, label, order in stats:
        ExperienceStat.objects.get_or_create(
            value=value,
            label=label,
            defaults={"sort_order": order, "is_active": True},
        )

    advantages = [
        (
            "contract",
            "Работа по договору",
            "Фиксируем обязательства и гарантию в договоре — вы знаете, за что платите и кто отвечает за результат.",
            0,
        ),
        (
            "wallet",
            "Смета без «раздуваний»",
            "Согласованный бюджет не меняется в процессе: никаких скрытых доплат и неожиданных статей.",
            1,
        ),
        (
            "sparkles",
            "Тест-драйв качества",
            "На замере бесплатно выполняем фрагмент работ — вы видите технологию и результат до подписания договора.",
            2,
        ),
        (
            "factory",
            "Собственное производство",
            "Изготавливаем плинтусы, фальшбалки и другие элементы — контролируем сроки и качество материалов.",
            3,
        ),
        (
            "certificate",
            "Сертифицированные материалы",
            "Используем проверенные ЛКМ и составы, в том числе премиальные линейки европейских производителей.",
            4,
        ),
        (
            "shield",
            "Гарантийное обслуживание",
            "Сопровождаем объект после сдачи: консультируем по уходу за деревом и оперативно выезжаем при необходимости.",
            5,
        ),
    ]
    for icon, title, description, order in advantages:
        ExperienceAdvantage.objects.get_or_create(
            title=title,
            defaults={
                "icon": icon,
                "description": description,
                "sort_order": order,
                "is_active": True,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_portfolio"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExperienceSection",
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
                        default="ОПЫТ И НАДЁЖНОСТЬ",
                        max_length=64,
                        verbose_name="Бейдж",
                    ),
                ),
                (
                    "title_prefix",
                    models.CharField(
                        default="Более",
                        max_length=80,
                        verbose_name="Заголовок (белая часть)",
                    ),
                ),
                (
                    "title_highlight",
                    models.CharField(
                        default="10 лет с деревом",
                        max_length=80,
                        verbose_name="Заголовок (акцент)",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        default=(
                            "Строительно-отделочная компания полного цикла для деревянных домов "
                            "в Москве и области — от шлифовки и покраски до кровли и инженерии."
                        ),
                        verbose_name="Краткое описание",
                    ),
                ),
                (
                    "story",
                    models.TextField(
                        default=(
                            "ArteMadera объединяет комплекс отделочных работ у одного исполнителя: "
                            "не нужно искать разных подрядчиков и согласовывать сроки. Работаем по договору "
                            "с фиксированной сметой, используем сертифицированные материалы и собственное "
                            "производство. На замере можем бесплатно показать качество — «тест-драйв» "
                            "на участке вашего дома."
                        ),
                        verbose_name="Текст о компании",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="experience/",
                        verbose_name="Фото (загрузка)",
                    ),
                ),
                (
                    "static_image",
                    models.CharField(
                        blank=True,
                        default="images/service-2.jpg",
                        max_length=200,
                        verbose_name="Фото из static",
                    ),
                ),
                (
                    "is_visible",
                    models.BooleanField(default=True, verbose_name="Показывать блок"),
                ),
            ],
            options={
                "verbose_name": "Блок «Опыт компании»",
                "verbose_name_plural": "Блок «Опыт компании»",
            },
        ),
        migrations.CreateModel(
            name="ExperienceStat",
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
                ("value", models.CharField(max_length=32, verbose_name="Значение")),
                ("label", models.CharField(max_length=120, verbose_name="Подпись")),
                ("sort_order", models.IntegerField(default=0, verbose_name="Порядок")),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Показывать"),
                ),
            ],
            options={
                "verbose_name": "Показатель опыта",
                "verbose_name_plural": "Показатели опыта",
                "ordering": ["sort_order", "pk"],
            },
        ),
        migrations.CreateModel(
            name="ExperienceAdvantage",
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
                ("title", models.CharField(max_length=120, verbose_name="Заголовок")),
                ("description", models.TextField(verbose_name="Описание")),
                (
                    "icon",
                    models.CharField(
                        choices=[
                            ("contract", "Договор"),
                            ("wallet", "Смета"),
                            ("shield", "Гарантия"),
                            ("sparkles", "Тест-драйв"),
                            ("factory", "Производство"),
                            ("certificate", "Сертификаты"),
                        ],
                        default="contract",
                        max_length=32,
                        verbose_name="Иконка",
                    ),
                ),
                ("sort_order", models.IntegerField(default=0, verbose_name="Порядок")),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Показывать"),
                ),
            ],
            options={
                "verbose_name": "Преимущество",
                "verbose_name_plural": "Преимущества (опыт)",
                "ordering": ["sort_order", "pk"],
            },
        ),
        migrations.RunPython(seed_experience, migrations.RunPython.noop),
    ]
