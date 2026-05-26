from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0018_sitepage_unified"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sitepage",
            name="hero_image",
            field=models.ImageField(
                blank=True,
                help_text="Кнопка загрузки справа — выберите файл, затем «Сохранить» внизу формы.",
                null=True,
                upload_to="pages/hero/",
                verbose_name="Загрузить фон",
            ),
        ),
        migrations.AlterField(
            model_name="sitepage",
            name="hero_static_image",
            field=models.CharField(
                blank=True,
                default="images/hero-bg.jpg",
                help_text="Используется только если выше не загружено изображение.",
                max_length=200,
                verbose_name="Запасной фон (файл в static)",
            ),
        ),
    ]
