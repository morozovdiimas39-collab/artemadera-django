from django.db import migrations


def update_home_obsada_image(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    Service.objects.filter(slug="obsada-okna-home").update(
        image="pages/hero/obsada-window-hero.webp",
        static_image="",
    )


def restore_home_obsada_image(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    Service.objects.filter(slug="obsada-okna-home").update(
        image="",
        static_image="images/quiz/quiz_brus_1776809793588.png",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0072_update_home_engineering_card"),
    ]

    operations = [
        migrations.RunPython(
            update_home_obsada_image,
            restore_home_obsada_image,
        ),
    ]
