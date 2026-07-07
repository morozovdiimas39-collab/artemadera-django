from django.db import migrations


def update_teplyy_shov_tiles(apps, schema_editor):
    SitePage = apps.get_model("main", "SitePage")
    Service = apps.get_model("main", "Service")
    PageServiceLink = apps.get_model("main", "PageServiceLink")

    page = SitePage.objects.filter(page_key="teplyy-shov").first()
    if not page:
        return

    rows = [
        {
            "slug": "teplyy-shov-rublenoe",
            "name": "Теплый шов для рубленного бревна",
            "description": "Герметизация швов строений из рубленного бревна",
            "url": "/teplyy-shov#quiz",
            "image": "pages/hero/1548c512-16f1-44ac-ab5f-c0bcd0881ee2.webp",
            "static_image": "",
            "layout": "wide",
        },
        {
            "slug": "teplyy-shov-ocil",
            "name": "Теплый шов для оцилиндровки",
            "description": "Герметизация швов строений из оцилиндрованного бревна",
            "url": "/teplyy-shov#quiz",
            "image": "",
            "static_image": "images/service-2.jpg",
            "layout": "",
        },
        {
            "slug": "teplyy-shov-brus",
            "name": "Теплый шов для бруса",
            "description": "Герметизация швов строений из бруса",
            "url": "/teplyy-shov#quiz",
            "image": "",
            "static_image": "images/portfolio-3.jpg",
            "layout": "",
        },
        {
            "slug": "teplyy-shov-preserve",
            "name": "Шлифовка с сохранением теплого шва",
            "description": "Выполняем профессиональную шлифовку, не повредив выполненный теплый шов",
            "url": "/shlifovka#quiz",
            "image": "",
            "static_image": "images/service-3.jpg",
            "layout": "wide",
        },
    ]

    PageServiceLink.objects.filter(page=page).delete()
    for index, row in enumerate(rows):
        service, _ = Service.objects.update_or_create(
            slug=row["slug"],
            defaults={
                "name": row["name"],
                "short_description": row["description"],
                "page_url": row["url"],
                "image": row["image"],
                "static_image": row["static_image"],
                "is_active": True,
            },
        )
        PageServiceLink.objects.create(
            page=page,
            service=service,
            sort_order=index,
            layout=row["layout"],
            is_visible=True,
        )

    SitePage.objects.filter(page_key="teplyy-shov").update(
        services_badge="Услуги",
        services_title_white="Герметизация",
        services_title_accent="межвенцовых швов",
        services_lead="Делаем тёплый шов с правильной подготовкой древесины, шнуром и аккуратной геометрией.",
    )


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0057_update_teplyy_shov_hero"),
    ]

    operations = [
        migrations.RunPython(update_teplyy_shov_tiles, noop_reverse),
    ]
