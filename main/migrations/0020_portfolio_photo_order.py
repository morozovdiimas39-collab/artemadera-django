from django.db import migrations, models


def normalize_portfolio_photos(apps, schema_editor):
    PortfolioProject = apps.get_model("main", "PortfolioProject")
    PortfolioProjectImage = apps.get_model("main", "PortfolioProjectImage")

    for project in PortfolioProject.objects.all():
        if not project.photos.exists() and (project.image or project.static_image):
            PortfolioProjectImage.objects.create(
                project=project,
                image=project.image,
                static_image=project.static_image or "",
                sort_order=0,
                is_cover=True,
                is_active=True,
            )

        photos = list(
            project.photos.filter(is_active=True).order_by("-is_cover", "sort_order", "pk")
        )
        for index, photo in enumerate(photos):
            photo.sort_order = index
            photo.is_cover = index == 0
            photo.save(update_fields=["sort_order", "is_cover"])


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0019_sitepage_hero_labels"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="portfolioprojectimage",
            options={
                "ordering": ["sort_order", "pk"],
                "verbose_name": "Фото",
                "verbose_name_plural": "Фото",
            },
        ),
        migrations.AlterField(
            model_name="portfolioproject",
            name="alt_text",
            field=models.CharField(blank=True, max_length=255, verbose_name="Alt (устарело)"),
        ),
        migrations.AlterField(
            model_name="portfolioproject",
            name="image",
            field=models.ImageField(
                blank=True,
                help_text="Не используется — загружайте фото в галерею ниже.",
                null=True,
                upload_to="portfolio/",
                verbose_name="Обложка (устарело)",
            ),
        ),
        migrations.AlterField(
            model_name="portfolioproject",
            name="static_image",
            field=models.CharField(
                blank=True,
                max_length=200,
                verbose_name="Обложка static (устарело)",
            ),
        ),
        migrations.AlterField(
            model_name="portfolioprojectimage",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="portfolio/cases/",
                verbose_name="Фото",
            ),
        ),
        migrations.AlterField(
            model_name="portfolioprojectimage",
            name="is_cover",
            field=models.BooleanField(
                default=False,
                editable=False,
                verbose_name="Обложка (служебное)",
            ),
        ),
        migrations.AlterField(
            model_name="portfolioprojectimage",
            name="sort_order",
            field=models.IntegerField(
                default=0,
                help_text="0 — обложка на карточке, дальше 1, 2, 3…",
                verbose_name="№",
            ),
        ),
        migrations.AlterField(
            model_name="portfolioprojectimage",
            name="static_image",
            field=models.CharField(
                blank=True,
                help_text="Только для старых записей: images/portfolio-1.jpg",
                max_length=200,
                verbose_name="Static (запас)",
            ),
        ),
        migrations.RunPython(normalize_portfolio_photos, migrations.RunPython.noop),
    ]
