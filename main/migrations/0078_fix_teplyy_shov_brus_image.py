from django.db import migrations


NEW_IMAGE = "services/teplyy-shov-brus-finished.webp"
OLD_IMAGE = "services/брус_2.webp"


def fix_teplyy_shov_brus_image(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    Service.objects.filter(slug="teplyy-shov-brus").update(
        image=NEW_IMAGE,
        static_image="",
    )


def restore_teplyy_shov_brus_image(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    Service.objects.filter(slug="teplyy-shov-brus").update(
        image=OLD_IMAGE,
        static_image="",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0077_fix_obsada_windows_doors_images"),
    ]

    operations = [
        migrations.RunPython(
            fix_teplyy_shov_brus_image,
            restore_teplyy_shov_brus_image,
        ),
    ]
