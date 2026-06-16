from django.db import migrations, models


def restore_work_process(apps, schema_editor):
    WorkProcessSection = apps.get_model("main", "WorkProcessSection")
    WorkProcessStep = apps.get_model("main", "WorkProcessStep")

    section, _ = WorkProcessSection.objects.get_or_create(pk=1)
    section.badge_text = "ЭТАПЫ РАБОТЫ"
    section.title_prefix = "Этапы"
    section.title_highlight = "нашей работы"
    section.description = (
        "От первого выезда до передачи объекта — четыре последовательных шага, "
        "понятных ещё до начала работ."
    )
    section.is_visible = True
    section.save()

    steps = [
        ("01", "Выезд на объект", "Осматриваем задачу, выполняем замеры и фиксируем пожелания."),
        ("02", "Смета и договор", "Согласуем объём, сроки и стоимость, закрепляем условия в договоре."),
        ("03", "Работы на объекте", "Выполняем работы по согласованной технологии и держим вас в курсе."),
        ("04", "Сдача объекта", "Проводим совместную приёмку, передаём результат и гарантию."),
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
        ("main", "0051_company_documents_and_process_text"),
    ]

    operations = [
        migrations.AlterField(
            model_name="workprocesssection",
            name="badge_text",
            field=models.CharField(
                default="ЭТАПЫ РАБОТЫ",
                max_length=64,
                verbose_name="Бейдж",
            ),
        ),
        migrations.RunPython(restore_work_process, migrations.RunPython.noop),
    ]
