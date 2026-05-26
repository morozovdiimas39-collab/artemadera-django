from django.db import migrations, models


def seed_shlifovka_page_services(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    SitePage = apps.get_model("main", "SitePage")
    PageServiceLink = apps.get_model("main", "PageServiceLink")

    page = SitePage.objects.filter(page_key="shlifovka").first()
    if not page:
        return

    SitePage.objects.filter(pk=page.pk).update(
        services_badge="Виды шлифовки",
        services_title_white="Комплексная ",
        services_title_accent="шлифовка домов",
        services_lead=(
            "Профессиональная шлифовка деревянных домов любой сложности — подготовим сруб, "
            "брус, бревно или лафет к покраске и долгой эксплуатации."
        ),
    )

    cards = [
        {
            "slug": "card-shlifovka-srub",
            "name": "Шлифовка срубов",
            "short_description": (
                "Шлифовка бревенчатых срубов: удаление старого покрытия, выравнивание и подготовка под финиш."
            ),
            "page_url": "/otdelka/shlifovka/sruba",
            "static_image": "images/service-1.jpg",
            "layout": "wide",
            "tag_override": "от 1 200 ₽/м²",
            "cta_label": "",
        },
        {
            "slug": "card-shlifovka-brus",
            "name": "Шлифовка бруса",
            "short_description": (
                "Шлифовка домов из профилированного и клееного бруса без повреждения геометрии."
            ),
            "page_url": "/otdelka/shlifovka/brusa",
            "static_image": "images/service-2.jpg",
            "layout": "",
            "tag_override": "от 1 100 ₽/м²",
            "cta_label": "",
        },
        {
            "slug": "card-shlifovka-ocil",
            "name": "Шлифовка оцилиндровки",
            "short_description": (
                "Шлифовка дома из оцилиндрованного бревна с сохранением естественной фактуры дерева."
            ),
            "page_url": "/otdelka/shlifovka/ocilindrovannogo-brevna",
            "static_image": "images/portfolio-1.jpg",
            "layout": "",
            "tag_override": "от 1 150 ₽/м²",
            "cta_label": "",
        },
        {
            "slug": "card-shlifovka-lafet",
            "name": "Шлифовка лафета",
            "short_description": (
                "Аккуратная шлифовка домов из лафета и плоскогранного бруса — ровная поверхность без сколов."
            ),
            "page_url": "/otdelka/shlifovka/lafeta",
            "static_image": "images/portfolio-2.jpg",
            "layout": "wide",
            "tag_override": "от 1 250 ₽/м²",
            "cta_label": "",
        },
        {
            "slug": "card-shlifovka-concierge",
            "name": "Консьержная шлифовка",
            "short_description": (
                "Финишная тонкая шлифовка перед покраской или пропиткой — идеально гладкая поверхность."
            ),
            "page_url": "/shlifovka#contact",
            "static_image": "images/service-3.jpg",
            "layout": "half",
            "tag_override": "от 800 ₽/м²",
            "cta_label": "",
        },
        {
            "slug": "card-shlifovka-banja",
            "name": "Шлифовка бань и саун",
            "short_description": (
                "Шлифовка деревянных бань и саун с учётом высоких температур и влажности."
            ),
            "page_url": "/shlifovka#quiz",
            "static_image": "images/portfolio-3.jpg",
            "layout": "half",
            "tag_override": "от 900 ₽/м²",
            "cta_label": "Рассчитать стоимость",
        },
    ]

    for i, row in enumerate(cards):
        slug = row.pop("slug")
        layout = row.pop("layout")
        tag_override = row.pop("tag_override")
        cta_label = row.pop("cta_label")
        svc, _ = Service.objects.update_or_create(
            slug=slug,
            defaults={
                **row,
                "description": row.get("short_description", ""),
                "is_active": True,
                "show_on_homepage": False,
                "order": 100 + i,
                "calculator_profile_id": None,
            },
        )
        PageServiceLink.objects.update_or_create(
            page=page,
            service=svc,
            defaults={
                "sort_order": i,
                "layout": layout,
                "tag_override": tag_override,
                "cta_label": cta_label,
                "is_visible": True,
            },
        )


def unseed(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    Service.objects.filter(slug__startswith="card-shlifovka-").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0028_experience_section_team_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="pageservicelink",
            name="cta_label",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Пусто — «Узнать подробнее».",
                max_length=80,
                verbose_name="Текст кнопки на карточке",
            ),
        ),
        migrations.AlterField(
            model_name="service",
            name="home_layout",
            field=models.CharField(
                blank=True,
                choices=[
                    ("", "Обычная"),
                    ("wide", "Широкая (2 колонки)"),
                    ("last", "Широкая в конце сетки"),
                    ("half", "Половина ряда (6/12)"),
                ],
                default="",
                help_text="Для страницы «Шлифовка» также задаёт ширину карточки в сетке блока услуг.",
                max_length=16,
                verbose_name="Раскладка на главной",
            ),
        ),
        migrations.AlterField(
            model_name="pageservicelink",
            name="layout",
            field=models.CharField(
                blank=True,
                choices=[
                    ("", "Обычная"),
                    ("wide", "Широкая (2 колонки)"),
                    ("last", "Широкая в конце сетки"),
                    ("half", "Половина ряда (6/12)"),
                ],
                default="",
                max_length=16,
                verbose_name="Раскладка карточки",
            ),
        ),
        migrations.RunPython(seed_shlifovka_page_services, unseed),
    ]
