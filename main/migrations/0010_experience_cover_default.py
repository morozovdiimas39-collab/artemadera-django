from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0009_blog"),
    ]

    operations = [
        migrations.AlterField(
            model_name="experiencesection",
            name="static_image",
            field=models.CharField(
                blank=True,
                default="images/hero-bg.jpg",
                max_length=200,
                verbose_name="Фото из static",
            ),
        ),
    ]
