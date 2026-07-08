from django.db import migrations


FINISHED_SEAM = "services/teplyy-shov-finished.webp"
OLD_FIRST_SHLIFOVKA = "images/service-1.jpg"
LAST_SHLIFOVKA = "services/c2bf2ee4-4a5a-4b7d-a660-49c5c9645167.webp"


def apply_images(apps, schema_editor):
    Service = apps.get_model("main", "Service")

    Service.objects.filter(slug="card-shlifovka-srub").update(
        image=LAST_SHLIFOVKA,
        static_image="",
    )
    Service.objects.filter(slug="card-shlifovka-pogonazh").update(
        image="",
        static_image=OLD_FIRST_SHLIFOVKA,
    )

    service_images = {
        "teplyy-shov-rublenoe": (FINISHED_SEAM, ""),
        "teplyy-shov-ocil": ("services/оцилиндовка_2.webp", ""),
        "teplyy-shov-brus": ("services/брус_2.webp", ""),
        "teplyy-shov-preserve": ("pages/hero/23b84e30-5a9c-45b5-acca-0462e07d96e2.webp", ""),
    }
    for slug, (image, static_image) in service_images.items():
        Service.objects.filter(slug=slug).update(image=image, static_image=static_image)


def revert_images(apps, schema_editor):
    Service = apps.get_model("main", "Service")

    Service.objects.filter(slug="card-shlifovka-srub").update(
        image="",
        static_image=OLD_FIRST_SHLIFOVKA,
    )
    Service.objects.filter(slug="card-shlifovka-pogonazh").update(
        image=LAST_SHLIFOVKA,
        static_image="",
    )
    Service.objects.filter(slug__startswith="teplyy-shov").update(
        image=FINISHED_SEAM,
        static_image="",
    )


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0066_remove_concierge_sanding"),
    ]

    operations = [
        migrations.RunPython(apply_images, revert_images),
    ]
