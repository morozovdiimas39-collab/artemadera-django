from django.db import migrations


WINDOW_IMAGE = "pages/hero/obsada-window-hero.webp"
DOOR_IMAGE = "services/obsada-doors-card.webp"


def fix_obsada_windows_doors_images(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    Service.objects.filter(slug__in=("obsada-okna", "obsada-okna-montazh")).update(
        image=WINDOW_IMAGE,
        static_image="",
    )
    Service.objects.filter(slug__in=("obsada-dveri", "obsada-dveri-montazh")).update(
        image=DOOR_IMAGE,
        static_image="",
    )


def restore_obsada_windows_doors_images(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    Service.objects.filter(slug="obsada-okna").update(
        image="pages/hero/2316ce5c-b962-41fa-971a-87e9528d1c4a.webp",
        static_image="",
    )
    Service.objects.filter(slug="obsada-dveri").update(
        image="pages/hero/2316ce5c-b962-41fa-971a-87e9528d1c4a_yLSXMX6.webp",
        static_image="",
    )
    Service.objects.filter(slug="obsada-okna-montazh").update(
        image="pages/hero/2316ce5c-b962-41fa-971a-87e9528d1c4a_yLSXMX6.webp",
        static_image="images/service-2.jpg",
    )
    Service.objects.filter(slug="obsada-dveri-montazh").update(
        image="pages/hero/2316ce5c-b962-41fa-971a-87e9528d1c4a_zI05m1D.webp",
        static_image="images/service-3.jpg",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0076_swap_after_sanding_paint_images"),
    ]

    operations = [
        migrations.RunPython(
            fix_obsada_windows_doors_images,
            restore_obsada_windows_doors_images,
        ),
    ]
