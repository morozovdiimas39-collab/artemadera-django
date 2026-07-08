from django.db import migrations


SANDING_IMAGE = "pages/hero/23b84e30-5a9c-45b5-acca-0462e07d96e2.webp"
PAINTING_IMAGE = "pages/hero/5955e59c-1584-42ec-ac89-d0b1ae9d1f03.webp"


def swap_after_sanding_paint_images(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    Service.objects.filter(slug__in=("after-sanding-paint", "pokraska-after-sanding")).update(
        image=PAINTING_IMAGE,
        static_image="",
    )
    Service.objects.filter(slug="walls-sanding").update(
        image=SANDING_IMAGE,
        static_image="",
    )


def restore_after_sanding_paint_images(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    Service.objects.filter(slug="after-sanding-paint").update(
        image="",
        static_image="images/service-3.jpg",
    )
    Service.objects.filter(slug="pokraska-after-sanding").update(
        image=SANDING_IMAGE,
        static_image="images/service-3.jpg",
    )
    Service.objects.filter(slug="walls-sanding").update(
        image=PAINTING_IMAGE,
        static_image="images/service-3.jpg",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0075_fix_after_sanding_service_images"),
    ]

    operations = [
        migrations.RunPython(
            swap_after_sanding_paint_images,
            restore_after_sanding_paint_images,
        ),
    ]
