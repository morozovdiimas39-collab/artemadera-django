from django.db import migrations


def apply_obsada_tiles(apps, schema_editor):
    SitePage = apps.get_model("main", "SitePage")
    Service = apps.get_model("main", "Service")
    PageServiceLink = apps.get_model("main", "PageServiceLink")

    page = SitePage.objects.filter(page_key="obsada").first()
    if not page:
        return

    Service.objects.filter(slug="obsada-dveri").update(
        name="Двери",
        short_description="Обсадные короба для входных и межкомнатных дверей с компенсацией усадки.",
        page_url="/obsada/dveri",
        is_active=True,
    )
    Service.objects.filter(slug="obsada-okna").update(
        name="Окна",
        short_description="Обсадные короба и подготовка оконных проёмов.",
        page_url="/obsada/okna",
        is_active=True,
    )
    Service.objects.filter(slug="teplyy-shov").update(
        name="Тёплый шов",
        short_description="Герметизация межвенцовых швов после установки окон и дверей.",
        page_url="/teplyy-shov",
        is_active=True,
    )

    PageServiceLink.objects.filter(page=page).delete()
    for order, slug in enumerate(("obsada-dveri", "obsada-okna", "teplyy-shov")):
        service = Service.objects.filter(slug=slug).first()
        if not service:
            continue
        PageServiceLink.objects.create(
            page=page,
            service=service,
            sort_order=order,
            layout="",
            is_visible=True,
        )


def revert_obsada_tiles(apps, schema_editor):
    SitePage = apps.get_model("main", "SitePage")
    Service = apps.get_model("main", "Service")
    PageServiceLink = apps.get_model("main", "PageServiceLink")

    page = SitePage.objects.filter(page_key="obsada").first()
    if not page:
        return

    Service.objects.filter(slug="obsada-dveri").update(name="Обсада дверей")
    PageServiceLink.objects.filter(page=page).delete()
    for order, (slug, layout) in enumerate(
        (
            ("obsada-okna", "wide"),
            ("obsada-dveri", ""),
            ("okosyachka", ""),
            ("teplyy-shov", "wide"),
        )
    ):
        service = Service.objects.filter(slug=slug).first()
        if not service:
            continue
        PageServiceLink.objects.create(
            page=page,
            service=service,
            sort_order=order,
            layout=layout,
            is_visible=True,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0061_update_obsada_hero_background"),
    ]

    operations = [
        migrations.RunPython(apply_obsada_tiles, revert_obsada_tiles),
    ]
