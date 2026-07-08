from django.db import migrations


def update_home_production_image(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    Service.objects.filter(slug="proizvodstvo-home").update(
        image="services/home-production-card.webp",
        static_image="",
    )


def restore_home_production_image(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    Service.objects.filter(slug="proizvodstvo-home").update(
        image="",
        static_image="images/portfolio-1.jpg",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0070_update_home_construction_image"),
    ]

    operations = [
        migrations.RunPython(
            update_home_production_image,
            restore_home_production_image,
        ),
    ]
