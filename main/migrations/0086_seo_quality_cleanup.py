from django.db import migrations


def clean_hero_headings(apps, schema_editor):
    SitePage = apps.get_model("main", "SitePage")
    updates = {
        "teplyy-shov": {
            "hero_h1_white": "Тёплый шов",
            "hero_h1_accent": "для деревянного дома",
        },
    }
    for page_key, values in updates.items():
        SitePage.objects.filter(page_key=page_key).update(**values)


def reverse_clean_hero_headings(apps, schema_editor):
    SitePage = apps.get_model("main", "SitePage")
    SitePage.objects.filter(page_key="teplyy-shov").update(
        hero_h1_white="Тёплый шов",
        hero_h1_accent="для деревянного\nдома",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0085_karkasnye_doma_page"),
    ]

    operations = [
        migrations.RunPython(clean_hero_headings, reverse_clean_hero_headings),
    ]
