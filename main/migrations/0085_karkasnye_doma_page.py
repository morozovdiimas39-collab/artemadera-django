from django.db import migrations


PAGE_KEY = "stroitelstvo/karkasnye-doma"
SEO_TITLE = "Строительство каркасных домов в Москве и МО | под ключ"
SEO_DESCRIPTION = (
    "Строительство каркасных домов под ключ в Москве и Московской области: "
    "проект, комплектация, тёплый контур, инженерия и отделка у одного подрядчика."
)


def apply_changes(apps, schema_editor):
    SitePage = apps.get_model("main", "SitePage")
    Service = apps.get_model("main", "Service")

    SitePage.objects.update_or_create(
        page_key=PAGE_KEY,
        defaults={
            "title": "Каркасные дома",
            "is_active": True,
            "sort_order": 95,
            "hero_static_image": "images/hero-bg.jpg",
            "hero_h1_white": "Строительство",
            "hero_h1_accent": "каркасных домов",
            "hero_lead": (
                "Каркасные дома под ключ в Москве и Московской области: проект, "
                "фундамент, тёплый контур, инженерия и отделка у одного подрядчика."
            ),
            "show_services_block": False,
            "seo_title": SEO_TITLE,
            "seo_description": SEO_DESCRIPTION,
            "seo_noindex": False,
        },
    )

    Service.objects.filter(slug="stroitelstvo").update(
        name="Строительство",
        short_description="Строительство каркасных домов полного цикла.",
        page_url=f"/{PAGE_KEY}",
        is_active=True,
    )


def restore_changes(apps, schema_editor):
    SitePage = apps.get_model("main", "SitePage")
    Service = apps.get_model("main", "Service")

    SitePage.objects.filter(page_key=PAGE_KEY).delete()
    Service.objects.filter(slug="stroitelstvo").update(
        short_description="Строительство деревянных домов полного цикла.",
        page_url="https://artemaderastroy.ru/",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0084_sitepage_seo_fields"),
    ]

    operations = [
        migrations.RunPython(apply_changes, restore_changes),
    ]
