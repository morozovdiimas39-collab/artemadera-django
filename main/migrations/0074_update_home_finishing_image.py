from django.db import migrations


def update_home_finishing_image(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    Service.objects.filter(slug="otdelochnye-raboty").update(
        image="services/finish-ceiling-cladding.webp",
        static_image="",
    )


def restore_home_finishing_image(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    Service.objects.filter(slug="otdelochnye-raboty").update(
        image="",
        static_image="images/service-2.jpg",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0073_update_home_obsada_image"),
    ]

    operations = [
        migrations.RunPython(
            update_home_finishing_image,
            restore_home_finishing_image,
        ),
    ]
