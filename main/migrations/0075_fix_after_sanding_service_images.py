from django.db import migrations


def fix_after_sanding_service_images(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    Service.objects.filter(slug="after-sanding-konopatka").update(
        image="",
        static_image="images/quiz/quiz_konopatka_1776809894304.png",
    )
    Service.objects.filter(slug="after-sanding-pogonazh").update(
        image="services/finish-decor-install.webp",
        static_image="",
    )


def restore_after_sanding_service_images(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    Service.objects.filter(slug="after-sanding-konopatka").update(
        image="",
        static_image="images/before.jpg",
    )
    Service.objects.filter(slug="after-sanding-pogonazh").update(
        image="",
        static_image="images/portfolio-1.jpg",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0074_update_home_finishing_image"),
    ]

    operations = [
        migrations.RunPython(
            fix_after_sanding_service_images,
            restore_after_sanding_service_images,
        ),
    ]
