from django.db import migrations


def apply_screenshot_edits(apps, schema_editor):
    SitePage = apps.get_model("main", "SitePage")
    Service = apps.get_model("main", "Service")
    PageServiceLink = apps.get_model("main", "PageServiceLink")

    def service(slug, name, description, url, image):
        obj, _ = Service.objects.update_or_create(
            slug=slug,
            defaults={
                "name": name,
                "short_description": description,
                "page_url": url,
                "static_image": image,
                "image": "",
                "is_active": True,
            },
        )
        return obj

    def set_page_services(page_key, rows):
        page = SitePage.objects.filter(page_key=page_key).first()
        if not page:
            return
        PageServiceLink.objects.filter(page=page).delete()
        for index, (slug, name, description, url, image, layout) in enumerate(rows):
            obj = service(slug, name, description, url, image)
            PageServiceLink.objects.create(
                page=page,
                service=obj,
                sort_order=index,
                layout=layout,
                is_visible=True,
            )

    sanding_rows = [
        ("card-shlifovka-srub", "Шлифовка срубов", "Удаление старого покрытия, выравнивание и подготовка сруба под финиш.", "/otdelka/shlifovka/sruba", "images/service-1.jpg", "wide"),
        ("card-shlifovka-brus", "Шлифовка бруса", "Шлифовка профилированного и клеёного бруса без повреждения геометрии.", "/otdelka/shlifovka/brusa", "images/service-2.jpg", ""),
        ("card-shlifovka-ocil", "Шлифовка оцилиндровки", "Сохраняем профиль бревна и естественную фактуру древесины.", "/otdelka/shlifovka/ocilindrovannogo-brevna", "images/portfolio-1.jpg", ""),
        ("card-shlifovka-lafet", "Шлифовка лафета", "Ровная поверхность лафета и плоскогранного бруса без сколов.", "/otdelka/shlifovka/lafeta", "images/portfolio-2.jpg", "wide"),
        ("card-shlifovka-pogonazh", "Шлифовка блок-хауса, имитации бруса и планкена", "Подготовка фасадных и погонажных изделий к покраске с сохранением профиля.", "/shlifovka#quiz", "images/service-3.jpg", "last"),
    ]
    set_page_services("shlifovka", sanding_rows)

    paint_rows = [
        ("pokraska-outside", "Покраска снаружи дома", "Профессиональная покраска стен и свесов с подбором ЛКМ. Предварительно выполняем выкрасы на объекте.", "/pokraska#quiz", "images/service-2.jpg", "wide"),
        ("pokraska-inside", "Покраска внутри дома", "Профессиональная покраска стен, потолков и пола с подбором ЛКМ.", "/pokraska#quiz", "images/portfolio-2.jpg", ""),
        ("pokraska-pogonazh", "Покраска погонажных изделий", "Покраска пиломатериалов, наличников, откосов, пергол и садовой мебели.", "/pokraska#quiz", "images/portfolio-3.jpg", ""),
        ("pokraska-renewal", "Обновление покрытия", "Обновляем покрытия для дерева без нарушения технологии, продлевая срок их службы.", "/pokraska#quiz", "images/after.jpg", "wide"),
    ]
    set_page_services("pokraska", paint_rows)

    seam_rows = [
        ("teplyy-shov-rublenoe", "Тёплый шов для рубленого бревна", "Герметизация швов строений из рубленого бревна.", "/teplyy-shov#quiz", "images/quiz/quiz_konopatka_1776809894304.png", "wide"),
        ("teplyy-shov-ocil", "Тёплый шов для оцилиндровки", "Герметизация швов строений из оцилиндрованного бревна.", "/teplyy-shov#quiz", "images/service-1.jpg", ""),
        ("teplyy-shov-brus", "Тёплый шов для бруса", "Герметизация швов строений из бруса.", "/teplyy-shov#quiz", "images/portfolio-3.jpg", ""),
        ("teplyy-shov-preserve", "Шлифовка с сохранением тёплого шва", "Профессионально шлифуем древесину, не повреждая выполненный тёплый шов.", "/shlifovka#quiz", "images/service-3.jpg", "wide"),
    ]
    set_page_services("teplyy-shov", seam_rows)

    finish_rows = [
        ("finish-floor", "Укладка пола", "Монтаж ламината, паркета и паркетной доски любой сложности.", "/otdelka/pola#quiz", "images/portfolio-2.jpg", "wide"),
        ("finish-ceiling", "Подшив потолка", "Монтаж планкена, имитации бруса, вагонки, гонта и гипсокартона.", "/otdelochnye-raboty#quiz", "images/portfolio-3.jpg", ""),
        ("finish-tile", "Укладка плитки", "Плитка на стены и пол: от крупного формата до мозаики.", "/otdelochnye-raboty#quiz", "images/after.jpg", ""),
        ("finish-partitions", "Монтаж перегородок", "Устройство перегородок и каркасов с различными видами отделки.", "/otdelochnye-raboty#quiz", "images/service-2.jpg", ""),
        ("finish-decor", "Монтаж декоративных элементов", "Установка наличников, фальшбалок, плинтусов и декоративных панелей.", "/proizvodstvo#contact", "images/service-3.jpg", ""),
        ("finish-steam-room", "Отделка парных", "Комплексное решение для парной с подбором материалов и всеми сопутствующими работами.", "/otdelochnye-raboty#quiz", "images/quiz/quiz_banja_modern_1776810582042.png", "wide"),
    ]
    set_page_services("otdelochnye-raboty", finish_rows)

    follow_up_rows = [
        ("after-sanding-paint", "Покраска после шлифовки", "Наносим грунты, масла, лазури и краски, соблюдая технологию производителя.", "/pokraska#quiz", "images/service-3.jpg", "wide"),
        ("after-sanding-seam", "Тёплый шов", "Герметизация наружных и внутренних межвенцовых швов.", "/teplyy-shov#quiz", "images/quiz/quiz_konopatka_1776809894304.png", ""),
        ("after-sanding-konopatka", "Конопатка", "Старорусский метод утепления бревенчатого дома.", "/otdelka/konopatka#quiz", "images/before.jpg", ""),
        ("after-sanding-pogonazh", "Монтаж погонажных изделий", "Установка наличников, накладок и других изделий. Устраняем производственные дефекты.", "/proizvodstvo#contact", "images/portfolio-1.jpg", "wide"),
    ]
    set_page_services("otdelka/shlifovka/sruba", follow_up_rows)
    set_page_services("otdelka/shlifovka/ocilindrovannogo-brevna", follow_up_rows)

    page_updates = {
        "pokraska": ("Услуги покраски", "деревянного дома", "Профессиональная покраска снаружи и внутри дома, погонажных изделий и обновление покрытий."),
        "teplyy-shov": ("Герметизация", "межвенцовых швов", "Делаем тёплый шов с правильной подготовкой древесины, шнурами и акрилатной геометрией."),
        "otdelochnye-raboty": ("Комплексная отделка", "деревянных домов", "Соберём нужные этапы в один понятный план: от пола и потолка до перегородок, плитки и декоративных элементов."),
    }
    for key, (white, accent, lead) in page_updates.items():
        SitePage.objects.filter(page_key=key).update(
            services_title_white=white,
            services_title_accent=accent,
            services_lead=lead,
        )

    SitePage.objects.filter(page_key="otdelochnye-raboty").update(
        hero_lead=(
            "Укладка пола, подшив потолка, монтаж перегородок, укладка плитки, "
            "изготовление и монтаж декоративных элементов."
        )
    )
    SitePage.objects.filter(page_key="teplyy-shov").update(
        hero_lead=(
            "Герметизация межвенцовых швов акриловыми герметиками. "
            "Устраняем продувы, сохраняем паропроницаемость и тепло в доме."
        ),
        hero_image="",
        hero_static_image="images/quiz/quiz_konopatka_1776809894304.png",
    )

    home_images = {
        "teplyy-shov": "images/quiz/quiz_konopatka_1776809894304.png",
        "obsada-okna-home": "images/quiz/quiz_brus_1776809793588.png",
        "injeneriya": "images/contact_bg.png",
        "stroitelstvo": "images/hero-bg.jpg",
        "proizvodstvo-home": "images/portfolio-1.jpg",
    }
    for slug, image in home_images.items():
        Service.objects.filter(slug=slug).update(image="", static_image=image)


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0054_about_company_process_and_home_services"),
    ]

    operations = [
        migrations.RunPython(apply_screenshot_edits, migrations.RunPython.noop),
    ]
