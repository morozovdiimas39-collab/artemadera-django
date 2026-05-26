from django.db import migrations


def shorten_first_two_steps(apps, schema_editor):
    WorkProcessStep = apps.get_model("main", "WorkProcessStep")
    WorkProcessStep.objects.filter(step_number="01").update(
        title="Выезд и согласование",
        description=(
            "Приезжаем на объект, уточняем задачи и фиксируем объём с ценой до старта работ по договору."
        ),
    )
    WorkProcessStep.objects.filter(step_number="02").update(
        title="Выполнение работ",
        description=(
            "Делаем всё по смете и этапам — соблюдаем технологию, сроки и аккуратность на площадке."
        ),
    )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0023_work_process_steps_shlifovka_text"),
    ]

    operations = [
        migrations.RunPython(shorten_first_two_steps, migrations.RunPython.noop),
    ]
