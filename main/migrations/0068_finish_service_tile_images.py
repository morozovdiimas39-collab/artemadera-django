from django.db import migrations


SERVICE_IMAGES = {
    "finish-floor": "services/finish-floor-install.webp",
    "finish-ceiling": "services/finish-ceiling-cladding.webp",
    "finish-tile": "services/finish-tile-install.webp",
    "finish-partitions": "services/finish-partitions-install.webp",
    "finish-decor": "services/finish-decor-install.webp",
    "finish-steam-room": "services/finish-steam-room.webp",
}


OLD_IMAGES = {
    "finish-floor": ("", "images/portfolio-2.jpg"),
    "finish-ceiling": ("", "images/portfolio-3.jpg"),
    "finish-tile": ("", "images/after.jpg"),
    "finish-partitions": ("", "images/service-2.jpg"),
    "finish-decor": ("", "images/service-3.jpg"),
    "finish-steam-room": ("", "images/quiz/quiz_banja_modern_1776810582042.png"),
}


def apply_finish_images(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    for slug, image in SERVICE_IMAGES.items():
        Service.objects.filter(slug=slug).update(image=image, static_image="")


def revert_finish_images(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    for slug, (image, static_image) in OLD_IMAGES.items():
        Service.objects.filter(slug=slug).update(
            image=image,
            static_image=static_image,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0067_teplyy_shov_images_and_shlifovka_swap"),
    ]

    operations = [
        migrations.RunPython(apply_finish_images, revert_finish_images),
    ]
