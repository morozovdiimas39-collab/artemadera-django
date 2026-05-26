from django.db import migrations


def forwards(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    SitePage = apps.get_model("main", "SitePage")

    Service.objects.filter(slug="card-shlifovka-concierge").update(
        page_url="/otdelka/shlifovka/konsyerzhnaya"
    )
    Service.objects.filter(slug="card-shlifovka-banja").update(
        page_url="/otdelka/shlifovka/bani-i-sauny"
    )

    pages = [
        (
            "otdelka/shlifovka/konsyerzhnaya",
            "Консьержная шлифовка",
            84,
            "images/service-3.jpg",
            "Консьержная",
            "шлифовка",
            "Финишная тонкая шлифовка перед покраской или пропиткой.",
        ),
        (
            "otdelka/shlifovka/bani-i-sauny",
            "Шлифовка бань и саун",
            85,
            "images/portfolio-3.jpg",
            "Шлифовка",
            "бань и саун",
            "Деревянные бани и сауны — с учётом высоких температур и влажности.",
        ),
    ]
    for page_key, title, sort_order, hero_static, h1w, h1a, lead in pages:
        SitePage.objects.update_or_create(
            page_key=page_key,
            defaults={
                "title": title,
                "sort_order": sort_order,
                "is_active": True,
                "show_services_block": False,
                "hero_static_image": hero_static,
                "hero_h1_white": h1w,
                "hero_h1_accent": h1a,
                "hero_lead": lead,
            },
        )


def backwards(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    SitePage = apps.get_model("main", "SitePage")

    Service.objects.filter(slug="card-shlifovka-concierge").update(page_url="/shlifovka#contact")
    Service.objects.filter(slug="card-shlifovka-banja").update(page_url="/shlifovka#quiz")
    SitePage.objects.filter(
        page_key__in=("otdelka/shlifovka/konsyerzhnaya", "otdelka/shlifovka/bani-i-sauny")
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0030_lead_email_settings"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
