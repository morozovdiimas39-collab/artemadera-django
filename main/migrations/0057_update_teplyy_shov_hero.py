from django.db import migrations


def update_teplyy_shov_hero(apps, schema_editor):
    SitePage = apps.get_model("main", "SitePage")
    SitePage.objects.filter(page_key="teplyy-shov").update(
        hero_image="pages/hero/1548c512-16f1-44ac-ab5f-c0bcd0881ee2.webp",
        hero_static_image="",
        hero_h1_white="Тёплый шов",
        hero_h1_accent="для деревянного\nдома",
        hero_lead=(
            "Герметизация межвенцовых швов акриловыми герметиками. "
            "Устраняем продувы, сохраняем паропроницаемость и тепло в доме."
        ),
    )


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0056_contactlead_pending_direct_status"),
    ]

    operations = [
        migrations.RunPython(update_teplyy_shov_hero, noop_reverse),
    ]
