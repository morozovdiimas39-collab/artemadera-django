from django.db import migrations, models

LEGACY_STATIC_IMAGES = (
    "images/service-2.jpg",
    "images/hero-bg.jpg",
    "images/after.jpg",
)


def forwards(apps, schema_editor):
    ExperienceSection = apps.get_model("main", "ExperienceSection")
    for row in ExperienceSection.objects.iterator():
        if row.image:
            continue
        if row.static_image in LEGACY_STATIC_IMAGES or not (row.static_image or "").strip():
            row.static_image = "images/team.png"
            row.save(update_fields=["static_image"])


def backwards(apps, schema_editor):
    ExperienceSection = apps.get_model("main", "ExperienceSection")
    for row in ExperienceSection.objects.iterator():
        if row.image:
            continue
        if row.static_image == "images/team.png":
            row.static_image = "images/after.jpg"
            row.save(update_fields=["static_image"])


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0027_contactlead_ym_client_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="experiencesection",
            name="static_image",
            field=models.CharField(
                blank=True,
                default="images/team.png",
                max_length=200,
                verbose_name="Фото из static",
            ),
        ),
        migrations.RunPython(forwards, backwards),
    ]
