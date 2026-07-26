from django.db import migrations


REMOVED_PAGE_KEYS = (
    "otdelka/shlifovka/bani-i-sauny",
    "otdelka/shlifovka/konsyerzhnaya",
)


def hide_removed_pages(apps, schema_editor):
    SitePage = apps.get_model("main", "SitePage")
    SitePage.objects.filter(page_key__in=REMOVED_PAGE_KEYS).update(
        is_active=False,
        seo_noindex=True,
    )


def restore_removed_pages(apps, schema_editor):
    SitePage = apps.get_model("main", "SitePage")
    SitePage.objects.filter(page_key__in=REMOVED_PAGE_KEYS).update(
        is_active=True,
        seo_noindex=False,
    )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0086_seo_quality_cleanup"),
    ]

    operations = [
        migrations.RunPython(hide_removed_pages, restore_removed_pages),
    ]
