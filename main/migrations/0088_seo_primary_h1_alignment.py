from django.db import migrations


def align_primary_h1(apps, schema_editor):
    SitePage = apps.get_model("main", "SitePage")
    updates = {
        "home": {
            "hero_h1_white": "Отделка",
            "hero_h1_accent": "деревянного дома",
        },
        "shlifovka": {
            "hero_h1_white": "Профессиональная шлифовка",
            "hero_h1_accent": "деревянного дома",
        },
        "injeneriya": {
            "hero_h1_white": "Инженерные коммуникации",
            "hero_h1_accent": "в деревянном доме",
        },
    }
    for page_key, values in updates.items():
        SitePage.objects.filter(page_key=page_key).update(**values)


def reverse_align_primary_h1(apps, schema_editor):
    SitePage = apps.get_model("main", "SitePage")
    SitePage.objects.filter(page_key="home").update(
        hero_h1_white="Отделка",
        hero_h1_accent="деревянных домов",
    )
    SitePage.objects.filter(page_key__in=("shlifovka", "injeneriya")).update(
        hero_h1_white="",
        hero_h1_accent="",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0087_hide_removed_shlifovka_pages"),
    ]

    operations = [
        migrations.RunPython(align_primary_h1, reverse_align_primary_h1),
    ]
