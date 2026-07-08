from django.db import migrations


def update_home_engineering_card(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    Service.objects.filter(slug="injeneriya").update(
        short_description="Инженерные коммуникации в деревянных домах.",
        image="services/home-engineering-card.webp",
        static_image="",
    )


def restore_home_engineering_card(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    Service.objects.filter(slug="injeneriya").update(
        short_description="Проектирование и монтаж инженерных систем.",
        image="",
        static_image="images/contact_bg.png",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0071_update_home_production_image"),
    ]

    operations = [
        migrations.RunPython(
            update_home_engineering_card,
            restore_home_engineering_card,
        ),
    ]
