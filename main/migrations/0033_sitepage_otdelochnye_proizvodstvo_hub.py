from django.db import migrations


def add_hub_sitepages(apps, schema_editor):
    SitePage = apps.get_model("main", "SitePage")
    hubs = [
        (
            68,
            "otdelochnye-raboty",
            "Отделочные работы",
            "Отделочные ",
            "работы",
            "Покраска, тёплый шов, конопатка и отделка деревянных домов — комплексно или отдельными видами работ.",
        ),
        (
            88,
            "proizvodstvo",
            "Производство",
            "Деревянное ",
            "производство",
            "Беседки, фальшбалки, плинтусы и другие изделия из дерева в мастерской ArteMadera.",
        ),
    ]
    for sort_order, page_key, title, h1w, h1a, lead in hubs:
        SitePage.objects.update_or_create(
            page_key=page_key,
            defaults={
                "title": title,
                "sort_order": sort_order,
                "is_active": True,
                "show_services_block": False,
                "hero_static_image": "images/hero-bg.jpg",
                "hero_h1_white": h1w,
                "hero_h1_accent": h1a,
                "hero_lead": lead,
            },
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0032_sitepage_services_badge_default"),
    ]

    operations = [
        migrations.RunPython(add_hub_sitepages, noop),
    ]
