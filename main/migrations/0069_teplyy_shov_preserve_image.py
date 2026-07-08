from django.db import migrations


NEW_IMAGE = "services/teplyy-shov-preserve-sanding.webp"
OLD_IMAGE = "pages/hero/23b84e30-5a9c-45b5-acca-0462e07d96e2.webp"


def apply_image(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    Service.objects.filter(slug="teplyy-shov-preserve").update(
        image=NEW_IMAGE,
        static_image="",
    )


def revert_image(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    Service.objects.filter(slug="teplyy-shov-preserve").update(
        image=OLD_IMAGE,
        static_image="",
    )


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0068_finish_service_tile_images"),
    ]

    operations = [
        migrations.RunPython(apply_image, revert_image),
    ]
