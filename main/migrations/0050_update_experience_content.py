from django.db import migrations, models


ADVANTAGES = [
    (
        "Превосходное качество",
        "Гарантируем превосходное качество покраски бруса.",
        "shield",
    ),
    (
        "Проверенные составы",
        "Используем только проверенные сертифицированные составы для покрытия.",
        "certificate",
    ),
    (
        "Большой опыт",
        "Уверенно берёмся за работу любой сложности.",
        "sparkles",
    ),
    (
        "Ответственный подход",
        "Честно и ответственно подходим к выполнению задачи.",
        "contract",
    ),
    (
        "Всегда на связи",
        "Даём исчерпывающую информацию о ходе работ и по запросу предоставляем фотоотчёт.",
        "factory",
    ),
]


def update_experience_content(apps, schema_editor):
    ExperienceSection = apps.get_model("main", "ExperienceSection")
    ExperienceAdvantage = apps.get_model("main", "ExperienceAdvantage")

    section, _ = ExperienceSection.objects.get_or_create(pk=1)
    section.badge_text = "ПОЧЕМУ ARTEMADERA"
    section.title_prefix = "Отвечаем"
    section.title_highlight = "за результат"
    section.description = "Работаем быстро, соблюдая сроки и не задерживая других подрядчиков."
    section.story = (
        "Честно и ответственно подходим к выполнению задачи. Заказчик получает "
        "исчерпывающую информацию о ходе работ, а по запросу — фотоотчёт с объекта."
    )
    section.save()

    ExperienceAdvantage.objects.all().delete()
    ExperienceAdvantage.objects.bulk_create(
        [
            ExperienceAdvantage(
                title=title,
                description=description,
                icon=icon,
                sort_order=index,
                is_active=True,
            )
            for index, (title, description, icon) in enumerate(ADVANTAGES, start=1)
        ]
    )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0049_portfolioproject_source_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="experiencesection",
            name="badge_text",
            field=models.CharField(
                default="ПОЧЕМУ ARTEMADERA", max_length=64, verbose_name="Бейдж"
            ),
        ),
        migrations.AlterField(
            model_name="experiencesection",
            name="description",
            field=models.TextField(
                default="Работаем быстро, соблюдая сроки и не задерживая других подрядчиков.",
                verbose_name="Краткое описание",
            ),
        ),
        migrations.AlterField(
            model_name="experiencesection",
            name="story",
            field=models.TextField(
                default=(
                    "Честно и ответственно подходим к выполнению задачи. Заказчик получает "
                    "исчерпывающую информацию о ходе работ, а по запросу — фотоотчёт с объекта."
                ),
                verbose_name="Текст о компании",
            ),
        ),
        migrations.AlterField(
            model_name="experiencesection",
            name="title_highlight",
            field=models.CharField(
                default="за результат",
                max_length=80,
                verbose_name="Заголовок (акцент)",
            ),
        ),
        migrations.AlterField(
            model_name="experiencesection",
            name="title_prefix",
            field=models.CharField(
                default="Отвечаем",
                max_length=80,
                verbose_name="Заголовок (белая часть)",
            ),
        ),
        migrations.RunPython(update_experience_content, migrations.RunPython.noop),
    ]
