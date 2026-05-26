from django.db import migrations


def rewrite_work_process_block(apps, schema_editor):
    WorkProcessSection = apps.get_model("main", "WorkProcessSection")
    WorkProcessStep = apps.get_model("main", "WorkProcessStep")

    WorkProcessSection.objects.filter(pk=1).update(
        description=(
            "От первого выезда до передачи объекта — четыре последовательных шага, "
            "понятных ещё до начала работ."
        ),
    )

    updates = {
        "01": (
            "Выезд на объект",
            "Осматриваем задачу и объём: замеры, фото, фиксация пожеланий — отправная точка для сметы.",
        ),
        "02": (
            "Смета и договор",
            "Считаем работы по этапам, согласуем сроки и цену, закрепляем всё в договоре — без скрытых условий.",
        ),
        "03": (
            "Работы на объекте",
            "Выполняем этапы по плану: технология, безопасность, порядок и промежуточные согласования по ходу.",
        ),
        "04": (
            "Сдача объекта",
            "Передаём результат: совместная приёмка, акты, рекомендации по уходу и гарантия на выполненные работы.",
        ),
    }
    for step_no, (title, description) in updates.items():
        WorkProcessStep.objects.filter(step_number=step_no).update(
            title=title,
            description=description,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0025_work_process_steps_general_scope"),
    ]

    operations = [
        migrations.RunPython(rewrite_work_process_block, migrations.RunPython.noop),
    ]
