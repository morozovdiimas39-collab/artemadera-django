from django.db import migrations, models
import django.db.models.deletion


def seed_home_services(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    CalculatorProfile = apps.get_model("main", "CalculatorProfile")

    def profile(slug):
        return CalculatorProfile.objects.filter(slug=slug).first()

    cards = [
        {
            "slug": "shlifovka",
            "name": "Шлифовка деревянных домов",
            "short_description": "Срубы, брус, оцилиндровка и лафет.",
            "description": "Шлифовка деревянных домов",
            "calculator_profile": profile("shlifovka"),
            "static_image": "images/quiz/quiz_shlifovka_1776809850085.png",
            "page_url": "/shlifovka",
            "home_layout": "wide",
            "order": 0,
        },
        {
            "slug": "pokraska",
            "name": "Покраска",
            "short_description": "Грунт, масла и лазури для фасада и интерьера.",
            "description": "Покраска",
            "calculator_profile": profile("pokraska"),
            "static_image": "images/quiz/quiz_pokraska_1776809864700.png",
            "home_tag_override": "под ключ",
            "page_url": "/pokraska",
            "order": 1,
        },
        {
            "slug": "teplyy-shov",
            "name": "Тёплый шов",
            "short_description": "Заполнение межвенцовых швов эластичным составом.",
            "description": "Тёплый шов",
            "calculator_profile": profile("teplyy-shov"),
            "static_image": "images/quiz/quiz_konopatka_1776809894304.png",
            "home_tag_override": "герметизация",
            "page_url": "/teplyy-shov",
            "order": 2,
        },
        {
            "slug": "okosyachka",
            "name": "Окосячка",
            "short_description": "Компенсация усадки, углы и каркас сруба.",
            "description": "Окосячка",
            "calculator_profile": profile("obsada"),
            "static_image": "images/quiz/quiz_srub_1776809774832.png",
            "home_tag_override": "усадка",
            "page_url": "/obsada",
            "order": 3,
        },
        {
            "slug": "obsada-okna",
            "name": "Обсада",
            "short_description": "Короба под окна и двери.",
            "description": "Обсада окон и дверей",
            "calculator_profile": profile("obsada"),
            "static_image": "images/quiz/quiz_brus_1776809793588.png",
            "home_tag_override": "проёмы",
            "page_url": "/obsada/okna",
            "order": 4,
        },
        {
            "slug": "kryshi",
            "name": "Крыши",
            "short_description": "Монтаж и ремонт кровли.",
            "description": "Крыши",
            "calculator_profile": profile("kryshi"),
            "static_image": "images/portfolio-3.jpg",
            "home_tag_override": "кровля",
            "page_url": "/kryshi",
            "order": 5,
        },
        {
            "slug": "injeneriya",
            "name": "Инженерия",
            "short_description": "Проект и монтаж инженерных систем.",
            "description": "Инженерия",
            "calculator_profile": profile("injeneriya"),
            "static_image": "images/after.jpg",
            "home_tag_override": "коммуникации",
            "page_url": "/injeneriya",
            "home_layout": "last",
            "order": 6,
        },
    ]

    for data in cards:
        calc = data.pop("calculator_profile", None)
        Service.objects.update_or_create(
            slug=data["slug"],
            defaults={
                **data,
                "calculator_profile_id": calc.pk if calc else None,
                "show_on_homepage": True,
                "is_active": True,
            },
        )


def unseed(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    slugs = [
        "shlifovka",
        "pokraska",
        "teplyy-shov",
        "okosyachka",
        "obsada-okna",
        "kryshi",
        "injeneriya",
    ]
    Service.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0015_blog_seed_posts"),
    ]

    operations = [
        migrations.AddField(
            model_name="service",
            name="calculator_profile",
            field=models.ForeignKey(
                blank=True,
                help_text="Минимальная цена из вариантов калькулятора — в бейдж на главной.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="homepage_services",
                to="main.calculatorprofile",
                verbose_name="Калькулятор",
            ),
        ),
        migrations.AddField(
            model_name="service",
            name="home_layout",
            field=models.CharField(
                blank=True,
                choices=[
                    ("", "Обычная"),
                    ("wide", "Широкая (2 колонки)"),
                    ("last", "Широкая в конце сетки"),
                ],
                default="",
                max_length=16,
                verbose_name="Раскладка на главной",
            ),
        ),
        migrations.AddField(
            model_name="service",
            name="home_tag_override",
            field=models.CharField(
                blank=True,
                help_text="Напр. «под ключ». Пусто — цена из калькулятора.",
                max_length=64,
                verbose_name="Бейдж на главной (вручную)",
            ),
        ),
        migrations.AddField(
            model_name="service",
            name="page_url",
            field=models.CharField(
                blank=True,
                help_text="Напр. /obsada/okna. Пусто — /slug/",
                max_length=200,
                verbose_name="Ссылка",
            ),
        ),
        migrations.AddField(
            model_name="service",
            name="show_on_homepage",
            field=models.BooleanField(default=False, verbose_name="Показывать на главной"),
        ),
        migrations.AddField(
            model_name="service",
            name="static_image",
            field=models.CharField(
                blank=True,
                help_text="Например images/quiz/quiz_shlifovka_1776809850085.png — если нет загрузки.",
                max_length=200,
                verbose_name="Фото (static)",
            ),
        ),
        migrations.AlterField(
            model_name="service",
            name="description",
            field=models.TextField(blank=True, verbose_name="Полное описание"),
        ),
        migrations.AlterField(
            model_name="service",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="services/",
                verbose_name="Фото на главной",
            ),
        ),
        migrations.AlterField(
            model_name="service",
            name="price_from",
            field=models.IntegerField(
                blank=True,
                help_text="Используется только если не выбран калькулятор и нет бейджа вручную.",
                null=True,
                verbose_name="Цена от (ручная, если нет калькулятора)",
            ),
        ),
        migrations.RunPython(seed_home_services, unseed),
    ]
