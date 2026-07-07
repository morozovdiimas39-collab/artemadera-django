from django.db import migrations


FINISHED_SEAM = "services/teplyy-shov-finished.webp"


def replace_teplyy_shov_images(apps, schema_editor):
    SitePage = apps.get_model("main", "SitePage")
    Service = apps.get_model("main", "Service")
    HomeQuizSettings = apps.get_model("main", "HomeQuizSettings")
    BlogPost = apps.get_model("main", "BlogPost")

    SitePage.objects.filter(page_key="teplyy-shov").update(
        hero_image=FINISHED_SEAM,
        hero_static_image="",
    )

    Service.objects.filter(slug__startswith="teplyy-shov").update(
        image=FINISHED_SEAM,
        static_image="",
    )
    Service.objects.filter(slug="after-sanding-seam").update(image=FINISHED_SEAM, static_image="")

    quiz, _ = HomeQuizSettings.objects.get_or_create(pk=1)
    quiz.image_teplyy_shov = FINISHED_SEAM
    quiz.save(update_fields=["image_teplyy_shov"])

    BlogPost.objects.filter(slug="chto-takoe-teplyy-shov").update(
        image=FINISHED_SEAM,
        static_image="",
    )


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0059_refresh_service_card_images"),
    ]

    operations = [
        migrations.RunPython(replace_teplyy_shov_images, noop_reverse),
    ]
