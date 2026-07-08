from django.db import migrations


LAST_TILE_IMAGE = "services/c2bf2ee4-4a5a-4b7d-a660-49c5c9645167.webp"


def apply_changes(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    PageServiceLink = apps.get_model("main", "PageServiceLink")

    Service.objects.filter(slug="card-shlifovka-srub").update(
        image=LAST_TILE_IMAGE,
        static_image="",
    )
    Service.objects.filter(slug="card-shlifovka-banja").update(is_active=False)
    PageServiceLink.objects.filter(service__slug="card-shlifovka-banja").update(
        is_visible=False
    )


def revert_changes(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    PageServiceLink = apps.get_model("main", "PageServiceLink")

    Service.objects.filter(slug="card-shlifovka-srub").update(
        image="",
        static_image="images/service-1.jpg",
    )
    Service.objects.filter(slug="card-shlifovka-banja").update(is_active=True)
    PageServiceLink.objects.filter(service__slug="card-shlifovka-banja").update(
        is_visible=True
    )


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0064_update_before_after_captions"),
    ]

    operations = [
        migrations.RunPython(apply_changes, revert_changes),
    ]
