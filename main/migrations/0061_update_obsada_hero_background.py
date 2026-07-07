from django.db import migrations


OBSADA_HERO = "pages/hero/obsada-window-hero.webp"


def apply_obsada_hero(apps, schema_editor):
    SitePage = apps.get_model("main", "SitePage")
    SitePage.objects.filter(page_key="obsada").update(
        hero_image=OBSADA_HERO,
        hero_static_image="",
    )


def revert_obsada_hero(apps, schema_editor):
    SitePage = apps.get_model("main", "SitePage")
    SitePage.objects.filter(page_key="obsada").update(
        hero_image="pages/hero/2316ce5c-b962-41fa-971a-87e9528d1c4a.webp",
        hero_static_image="",
    )


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0060_replace_teplyy_shov_finished_image"),
    ]

    operations = [
        migrations.RunPython(apply_obsada_hero, revert_obsada_hero),
    ]
