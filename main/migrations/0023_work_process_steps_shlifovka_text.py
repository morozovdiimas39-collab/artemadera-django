from django.db import migrations


def update_first_two_steps(apps, schema_editor):
    WorkProcessStep = apps.get_model("main", "WorkProcessStep")
    mapping = {
        "01": (
            "Выезд и согласование",
            "Приезжаем на объект, уточняем задачи и фиксируем объём с ценой до старта работ по договору.",
        ),
        "02": (
            "Выполнение работ",
            "Делаем всё по смете и этапам — соблюдаем технологию, сроки и аккуратность на площадке.",
        ),
    }
    for step_no, (title, description) in mapping.items():
        WorkProcessStep.objects.filter(step_number=step_no).update(
            title=title,
            description=description,
        )


def restore_old_steps(apps, schema_editor):
    WorkProcessStep = apps.get_model("main", "WorkProcessStep")
    WorkProcessStep.objects.filter(step_number="01").update(
        title="Замер и выкрас",
        description=(
            "Приезжаем на объект для точных замеров и бесплатно выполняем тестовую "
            "покраску прямо на вашем доме — вы видите результат до договора."
        ),
    )
    WorkProcessStep.objects.filter(step_number="02").update(
        title="Без проживания",
        description=(
            "Работаем мобильными бригадами: мастера полностью автономны и не требуют "
            "от вас жилья или условий для проживания на объекте."
        ),
    )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0022_blogpost_slug_unique"),
    ]

    operations = [
        migrations.RunPython(update_first_two_steps, restore_old_steps),
    ]
