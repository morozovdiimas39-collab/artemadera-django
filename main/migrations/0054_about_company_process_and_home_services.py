from django.db import migrations, models


ABOUT_DESCRIPTION = (
    "Строительно-отделочная компания полного цикла для деревянных домов "
    "в любом регионе нашей страны — от строительства до профессиональной "
    "отделки и инженерии."
)

ABOUT_STORY = (
    "ArteMadera объединяет комплекс строительных и отделочных работ у одного "
    "исполнителя: не нужно искать разных подрядчиков и согласовывать сроки. "
    "Работаем по договору с фиксированной сметой, используем сертифицированные "
    "материалы и собственное производство. На замере можем бесплатно показать "
    "качество — «тест-драйв» на участке вашего дома."
)


def update_company_content(apps, schema_editor):
    ExperienceSection = apps.get_model("main", "ExperienceSection")
    ExperienceStat = apps.get_model("main", "ExperienceStat")
    WorkProcessSection = apps.get_model("main", "WorkProcessSection")
    WorkProcessStep = apps.get_model("main", "WorkProcessStep")
    SitePage = apps.get_model("main", "SitePage")
    Service = apps.get_model("main", "Service")
    PageServiceLink = apps.get_model("main", "PageServiceLink")

    section, _ = ExperienceSection.objects.get_or_create(pk=1)
    section.badge_text = "ОПЫТ И НАДЁЖНОСТЬ"
    section.title_prefix = "Более 10 лет"
    section.title_highlight = "с деревом"
    section.description = ABOUT_DESCRIPTION
    section.story = ABOUT_STORY
    section.is_visible = True
    section.save()

    stats = [
        ("10+", "Лет на рынке"),
        ("500+", "Выполненных объектов"),
        ("1", "Подрядчик на весь цикл"),
        ("3 года", "Гарантия на работы"),
        ("Своё", "Собственное производство"),
        ("Своя", "Площадка для сборки домов"),
    ]
    ExperienceStat.objects.all().delete()
    ExperienceStat.objects.bulk_create(
        [
            ExperienceStat(value=value, label=label, sort_order=index, is_active=True)
            for index, (value, label) in enumerate(stats, start=1)
        ]
    )

    process, _ = WorkProcessSection.objects.get_or_create(pk=1)
    process.description = (
        "От первого выезда до постгарантийной поддержки — пять последовательных "
        "шагов, понятных ещё до начала работ."
    )
    process.is_visible = True
    process.save()
    WorkProcessStep.objects.update_or_create(
        step_number="05",
        defaults={
            "title": "Постгарантийное обслуживание",
            "description": (
                "Остаёмся на связи после завершения работ, консультируем по уходу "
                "и оперативно помогаем при необходимости."
            ),
            "sort_order": 5,
            "is_active": True,
        },
    )

    SitePage.objects.update_or_create(
        page_key="o-kompanii",
        defaults={
            "title": "О компании",
            "sort_order": 5,
            "show_services_block": False,
            "hero_static_image": "images/hero-bg.jpg",
            "is_active": True,
        },
    )
    home, _ = SitePage.objects.get_or_create(
        page_key="home",
        defaults={"title": "Главная", "is_active": True},
    )

    service_rows = [
        ("shlifovka", "Шлифовка", "Срубы, брус, оцилиндровка и лафет.", "/shlifovka", "images/quiz/quiz_shlifovka_1776809850085.png"),
        ("pokraska", "Покраска", "Грунт, масла и лазури для фасада и интерьера.", "/pokraska", "images/quiz/quiz_pokraska_1776809864700.png"),
        ("teplyy-shov", "Тёплый шов", "Герметизация межвенцовых швов.", "/teplyy-shov", "images/quiz/quiz_konopatka_1776809894304.png"),
        ("otdelochnye-raboty", "Отделочные работы", "Комплексная внутренняя и внешняя отделка деревянных домов.", "/otdelochnye-raboty", "images/service-2.jpg"),
        ("obsada-okna-home", "Обсада / окна", "Обсадные короба и подготовка оконных проёмов.", "/obsada", "images/quiz/quiz_brus_1776809793588.png"),
        ("kryshi", "Крыши", "Монтаж, ремонт и утепление кровли.", "/kryshi", "images/portfolio-3.jpg"),
        ("injeneriya", "Инженерия", "Проектирование и монтаж инженерных систем.", "/injeneriya", "images/after.jpg"),
        ("stroitelstvo", "Строительство", "Строительство деревянных домов полного цикла.", "https://artemaderastroy.ru/", "images/hero-bg.jpg"),
        ("proizvodstvo-home", "Производство", "Собственное производство изделий из дерева под проект.", "/proizvodstvo", "images/portfolio-1.jpg"),
    ]

    PageServiceLink.objects.filter(page=home).delete()
    for index, (slug, name, description, url, image) in enumerate(service_rows):
        service, _ = Service.objects.update_or_create(
            slug=slug,
            defaults={
                "name": name,
                "short_description": description,
                "page_url": url,
                "static_image": image,
                "home_layout": "",
                "show_on_homepage": True,
                "order": index,
                "is_active": True,
            },
        )
        PageServiceLink.objects.create(
            page=home,
            service=service,
            sort_order=index,
            layout="",
            is_visible=True,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0053_remove_companydocument"),
    ]

    operations = [
        migrations.AlterField(
            model_name="experiencesection",
            name="badge_text",
            field=models.CharField(default="ОПЫТ И НАДЁЖНОСТЬ", max_length=64, verbose_name="Бейдж"),
        ),
        migrations.AlterField(
            model_name="experiencesection",
            name="description",
            field=models.TextField(default=ABOUT_DESCRIPTION, verbose_name="Краткое описание"),
        ),
        migrations.AlterField(
            model_name="experiencesection",
            name="story",
            field=models.TextField(default=ABOUT_STORY, verbose_name="Текст о компании"),
        ),
        migrations.AlterField(
            model_name="experiencesection",
            name="title_highlight",
            field=models.CharField(default="с деревом", max_length=80, verbose_name="Заголовок (акцент)"),
        ),
        migrations.AlterField(
            model_name="experiencesection",
            name="title_prefix",
            field=models.CharField(default="Более 10 лет", max_length=80, verbose_name="Заголовок (белая часть)"),
        ),
        migrations.AlterField(
            model_name="workprocesssection",
            name="description",
            field=models.TextField(
                default=(
                    "От первого выезда до постгарантийной поддержки — пять последовательных "
                    "шагов, понятных ещё до начала работ."
                ),
                verbose_name="Описание",
            ),
        ),
        migrations.RunPython(update_company_content, migrations.RunPython.noop),
    ]
