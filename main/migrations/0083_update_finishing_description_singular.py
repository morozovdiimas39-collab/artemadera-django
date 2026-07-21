from django.db import migrations


OLD_TEXT = "Комплексная внутренняя и внешняя отделка деревянных домов."
NEW_TEXT = "Комплексная внутренняя и внешняя отделка деревянного дома."


def apply_change(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    Service.objects.filter(
        slug="otdelochnye-raboty",
        short_description=OLD_TEXT,
    ).update(short_description=NEW_TEXT)


def restore_change(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    Service.objects.filter(
        slug="otdelochnye-raboty",
        short_description=NEW_TEXT,
    ).update(short_description=OLD_TEXT)


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0082_production_hero_and_ads_smtp"),
    ]

    operations = [
        migrations.RunPython(apply_change, restore_change),
    ]
