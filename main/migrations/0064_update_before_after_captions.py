from django.db import migrations


def apply_captions(apps, schema_editor):
    BeforeAfterItem = apps.get_model("main", "BeforeAfterItem")
    BeforeAfterItem.objects.filter(title="Шлифовка сруба").update(title="Шлифовка")
    BeforeAfterItem.objects.filter(title="Дом из бруса").update(title="Дом из ОЦБ")


def revert_captions(apps, schema_editor):
    BeforeAfterItem = apps.get_model("main", "BeforeAfterItem")
    BeforeAfterItem.objects.filter(title="Шлифовка").update(title="Шлифовка сруба")
    BeforeAfterItem.objects.filter(title="Дом из ОЦБ").update(title="Дом из бруса")


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0063_obsada_before_after_images"),
    ]

    operations = [
        migrations.RunPython(apply_captions, revert_captions),
    ]
