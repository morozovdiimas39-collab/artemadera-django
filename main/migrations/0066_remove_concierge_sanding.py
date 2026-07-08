from django.db import migrations


def apply_remove_concierge(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    PageServiceLink = apps.get_model("main", "PageServiceLink")

    Service.objects.filter(slug="card-shlifovka-concierge").update(is_active=False)
    PageServiceLink.objects.filter(service__slug="card-shlifovka-concierge").update(
        is_visible=False
    )


def revert_remove_concierge(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    PageServiceLink = apps.get_model("main", "PageServiceLink")

    Service.objects.filter(slug="card-shlifovka-concierge").update(is_active=True)
    PageServiceLink.objects.filter(service__slug="card-shlifovka-concierge").update(
        is_visible=True
    )


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0065_shlifovka_tiles_and_remove_sauna"),
    ]

    operations = [
        migrations.RunPython(apply_remove_concierge, revert_remove_concierge),
    ]
