from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0020_portfolio_photo_order"),
    ]

    operations = [
        migrations.CreateModel(
            name="HomeQuizSettings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "default_image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="home_quiz/",
                        verbose_name="Фото по умолчанию (до выбора)",
                    ),
                ),
                (
                    "image_shlifovka",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="home_quiz/",
                        verbose_name="Шлифовка",
                    ),
                ),
                (
                    "image_pokraska",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="home_quiz/",
                        verbose_name="Покраска",
                    ),
                ),
                (
                    "image_teplyy_shov",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="home_quiz/",
                        verbose_name="Тёплый шов",
                    ),
                ),
                (
                    "image_okosyachka",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="home_quiz/",
                        verbose_name="Окосячка",
                    ),
                ),
                (
                    "image_obsada",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="home_quiz/",
                        verbose_name="Обсада",
                    ),
                ),
                (
                    "image_kryshi",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="home_quiz/",
                        verbose_name="Крыши",
                    ),
                ),
                (
                    "image_injeneriya",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="home_quiz/",
                        verbose_name="Инженерия",
                    ),
                ),
            ],
            options={
                "verbose_name": "Квиз на главной — картинки",
                "verbose_name_plural": "Квиз на главной — картинки",
            },
        ),
    ]
