from django.db import migrations


NEW_IMAGES = {
    "engineer-electric": "services/engineering-electric-card.webp",
    "engineer-heating": "services/engineering-heating-card.webp",
    "engineer-water": "services/engineering-water-card.webp",
    "engineer-vent": "services/engineering-vent-card.webp",
}

OLD_IMAGES = {
    "engineer-electric": ("portfolio/cases/6.webp", "images/portfolio-1.jpg"),
    "engineer-heating": ("portfolio/cases/5.webp", "images/portfolio-2.jpg"),
    "engineer-water": ("portfolio/cases/6.webp", "images/portfolio-3.jpg"),
    "engineer-vent": ("services/7.webp", "images/service-3.jpg"),
}


def fix_engineering_service_images(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    for slug, image in NEW_IMAGES.items():
        Service.objects.filter(slug=slug).update(image=image, static_image="")


def restore_engineering_service_images(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    for slug, (image, static_image) in OLD_IMAGES.items():
        Service.objects.filter(slug=slug).update(
            image=image,
            static_image=static_image,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0078_fix_teplyy_shov_brus_image"),
    ]

    operations = [
        migrations.RunPython(
            fix_engineering_service_images,
            restore_engineering_service_images,
        ),
    ]
