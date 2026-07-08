from django.db import migrations


def update_home_construction_image(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    Service.objects.filter(slug="stroitelstvo").update(
        image="services/home-construction-card.webp",
        static_image="",
    )


def restore_home_construction_image(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    Service.objects.filter(slug="stroitelstvo").update(
        image="",
        static_image="images/hero-bg.jpg",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0069_teplyy_shov_preserve_image"),
    ]

    operations = [
        migrations.RunPython(
            update_home_construction_image,
            restore_home_construction_image,
        ),
    ]
