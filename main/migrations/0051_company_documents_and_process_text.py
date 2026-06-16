from django.db import migrations, models


def update_process_text(apps, schema_editor):
    WorkProcessSection = apps.get_model("main", "WorkProcessSection")
    WorkProcessStep = apps.get_model("main", "WorkProcessStep")

    section, _ = WorkProcessSection.objects.get_or_create(pk=1)
    section.badge_text = "КАК МЫ РАБОТАЕМ"
    section.title_prefix = "Как мы"
    section.title_highlight = "работаем"
    section.description = "Четыре понятных этапа — от первой заявки до сдачи готового объекта."
    section.is_visible = True
    section.save()

    steps = [
        ("01", "Заявка", "Вы оставляете заявку на выезд менеджера."),
        ("02", "Оценка и смета", "Менеджер оценивает объём работы и составляет смету."),
        ("03", "Выполнение", "Выполняем работу в оговоренные сроки по договору."),
        ("04", "Завершение", "Сдаём вам готовый объект."),
    ]
    WorkProcessStep.objects.all().delete()
    WorkProcessStep.objects.bulk_create(
        [
            WorkProcessStep(
                step_number=number,
                title=title,
                description=description,
                sort_order=index,
                is_active=True,
            )
            for index, (number, title, description) in enumerate(steps, start=1)
        ]
    )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0050_update_experience_content"),
    ]

    operations = [
        migrations.CreateModel(
            name="CompanyDocument",
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
                ("title", models.CharField(max_length=160, verbose_name="Название")),
                (
                    "description",
                    models.CharField(blank=True, max_length=240, verbose_name="Описание"),
                ),
                (
                    "file",
                    models.FileField(
                        blank=True,
                        help_text="Обычно PDF. Если файл не загружен, карточка ведёт к форме заявки.",
                        null=True,
                        upload_to="company/documents/",
                        verbose_name="Файл",
                    ),
                ),
                ("sort_order", models.IntegerField(default=0, verbose_name="Порядок")),
                ("is_active", models.BooleanField(default=True, verbose_name="Показывать")),
            ],
            options={
                "verbose_name": "Документ компании",
                "verbose_name_plural": "Документы компании",
                "ordering": ["sort_order", "pk"],
            },
        ),
        migrations.RunPython(update_process_text, migrations.RunPython.noop),
    ]
