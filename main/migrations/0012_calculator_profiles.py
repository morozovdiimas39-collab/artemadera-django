from django.db import migrations, models
import django.db.models.deletion


def seed_profiles(apps, schema_editor):
    CalculatorProfile = apps.get_model("main", "CalculatorProfile")
    CalculatorOption = apps.get_model("main", "CalculatorOption")
    CalculatorServiceChoice = apps.get_model("main", "CalculatorServiceChoice")
    CalculatorMaterial = apps.get_model("main", "CalculatorMaterial")
    CalculatorConfig = apps.get_model("main", "CalculatorConfig")

    cfg, _ = CalculatorConfig.objects.get_or_create(pk=1)

    def upsert_profile(slug, **fields):
        defaults = {
            "area_min": cfg.area_min,
            "area_max": cfg.area_max,
            "area_step": cfg.area_step,
            "area_default": cfg.area_default,
            "is_active": True,
        }
        defaults.update(fields)
        return CalculatorProfile.objects.update_or_create(slug=slug, defaults=defaults)[0]

    shlifovka = upsert_profile(
        "shlifovka",
        name="Шлифовка",
        title="Калькулятор шлифовки",
        description="Узнайте примерную стоимость шлифовки. Точную смету рассчитаем после осмотра объекта.",
        options_label="Материал дома",
        unit_type="sqm",
        unit_label="м²",
    )
    for mat in CalculatorMaterial.objects.all().order_by("sort_order", "pk"):
        CalculatorOption.objects.update_or_create(
            profile=shlifovka,
            key=mat.key,
            defaults={
                "label": mat.label,
                "price_per_unit": mat.price_per_sqm,
                "sort_order": mat.sort_order,
                "is_active": mat.is_active,
            },
        )
    if not CalculatorOption.objects.filter(profile=shlifovka).exists():
        for key, label, price, order in [
            ("srub", "Сруб (бревенчатый)", 1200, 0),
            ("brus", "Дом из бруса", 1100, 1),
            ("kleen", "Клееный брус", 1000, 2),
            ("banya", "Баня/сауна", 1500, 3),
        ]:
            CalculatorOption.objects.create(
                profile=shlifovka,
                key=key,
                label=label,
                price_per_unit=price,
                sort_order=order,
                is_active=True,
            )

    pokraska = upsert_profile(
        "pokraska",
        name="Покраска",
        title="Калькулятор покраски",
        description="Примерная стоимость покраски деревянного дома маслом или лазурью.",
        options_label="Тип покрытия",
        unit_type="sqm",
        unit_label="м²",
        sort_order=1,
    )
    for key, label, price, order in [
        ("oil", "Масло", 650, 0),
        ("lazur", "Лазурь", 750, 1),
        ("antisept", "Антисептик + грунт", 550, 2),
        ("complex", "Комплекс (2 слоя)", 1100, 3),
    ]:
        CalculatorOption.objects.update_or_create(
            profile=pokraska,
            key=key,
            defaults={"label": label, "price_per_unit": price, "sort_order": order, "is_active": True},
        )

    teplyy = upsert_profile(
        "teplyy-shov",
        name="Тёплый шов",
        title="Калькулятор тёплого шва",
        description="Расчёт по погонным метрам межвенцовых швов.",
        options_label="Тип шва",
        unit_type="linear",
        unit_label="м.п.",
        area_min=20,
        area_max=500,
        area_default=120,
        sort_order=2,
    )
    for key, label, price, order in [
        ("standard", "Стандартный шов", 350, 0),
        ("premium", "Премиум герметик", 480, 1),
    ]:
        CalculatorOption.objects.update_or_create(
            profile=teplyy,
            key=key,
            defaults={"label": label, "price_per_unit": price, "sort_order": order, "is_active": True},
        )

    obsada = upsert_profile(
        "obsada",
        name="Обсада",
        title="Калькулятор обсады",
        description="Ориентировочная стоимость окосячки и подготовки проёмов.",
        options_label="Тип работ",
        unit_type="fixed",
        unit_label="",
        area_min=1,
        area_max=1,
        area_default=1,
        sort_order=3,
    )
    for key, label, price, order in [
        ("okosyachka", "Обсада / окосячка", 85000, 0),
        ("okna", "Окна (проём)", 12000, 1),
        ("dveri", "Двери (проём)", 15000, 2),
    ]:
        CalculatorOption.objects.update_or_create(
            profile=obsada,
            key=key,
            defaults={"label": label, "price_per_unit": price, "sort_order": order, "is_active": True},
        )

    kryshi = upsert_profile(
        "kryshi",
        name="Крыши",
        title="Калькулятор кровельных работ",
        description="Примерная стоимость в зависимости от типа кровли.",
        options_label="Тип кровли",
        unit_type="sqm",
        unit_label="м²",
        sort_order=4,
    )
    for key, label, price, order in [
        ("metall", "Металлочерепица", 1800, 0),
        ("gibkaya", "Гибкая черепица", 2200, 1),
        ("remont", "Ремонт кровли", 1200, 2),
    ]:
        CalculatorOption.objects.update_or_create(
            profile=kryshi,
            key=key,
            defaults={"label": label, "price_per_unit": price, "sort_order": order, "is_active": True},
        )

    injeneriya = upsert_profile(
        "injeneriya",
        name="Инженерия",
        title="Калькулятор инженерных работ",
        description="Ориентир по стоимости проектирования и монтажа.",
        options_label="Комплектация",
        unit_type="fixed",
        unit_label="",
        area_min=1,
        area_max=1,
        area_default=1,
        sort_order=5,
    )
    for key, label, price, order in [
        ("project", "Проект", 45000, 0),
        ("montazh", "Монтаж под ключ", 180000, 1),
    ]:
        CalculatorOption.objects.update_or_create(
            profile=injeneriya,
            key=key,
            defaults={"label": label, "price_per_unit": price, "sort_order": order, "is_active": True},
        )

    home = upsert_profile(
        "home",
        name="Главная",
        title="Подберём услугу и рассчитаем стоимость",
        description="Выберите направление работ — покажем калькулятор с ориентировочной ценой.",
        badge_text="РАСЧЁТ СТОИМОСТИ",
        show_service_picker=True,
        sort_order=-1,
    )

    choices = [
        ("Шлифовка", shlifovka, "Срубы, брус, лафет", 0),
        ("Покраска", pokraska, "Масла и лазури", 1),
        ("Тёплый шов", teplyy, "Герметизация швов", 2),
        ("Обсада", obsada, "Окосячка, окна, двери", 3),
        ("Крыши", kryshi, "Монтаж и ремонт", 4),
        ("Инженерия", injeneriya, "Проект и монтаж", 5),
    ]
    for label, target, hint, order in choices:
        CalculatorServiceChoice.objects.update_or_create(
            profile=home,
            label=label,
            defaults={
                "target_profile_id": target.id,
                "hint": hint,
                "sort_order": order,
                "is_active": True,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0011_alter_contactsection_description"),
    ]

    operations = [
        migrations.CreateModel(
            name="CalculatorProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("slug", models.SlugField(max_length=48, unique=True, verbose_name="Код страницы (home, shlifovka, pokraska…)")),
                ("name", models.CharField(max_length=120, verbose_name="Название в админке")),
                ("badge_text", models.CharField(default="КАЛЬКУЛЯТОР", max_length=64, verbose_name="Бейдж")),
                ("title", models.CharField(default="Онлайн-калькулятор", max_length=120, verbose_name="Заголовок")),
                ("description", models.TextField(default="Узнайте примерную стоимость. Точную смету рассчитаем после осмотра.", verbose_name="Описание")),
                ("perk_1", models.CharField(default="Бесплатный расчёт — под ваш объект", max_length=200, verbose_name="Преимущество 1")),
                ("perk_2", models.CharField(default="Перезвон за 30 минут", max_length=200, verbose_name="Преимущество 2")),
                ("perk_3", models.CharField(default="Консультация по срокам и этапам", max_length=200, verbose_name="Преимущество 3")),
                ("options_label", models.CharField(default="Материал дома", max_length=120, verbose_name="Подпись блока вариантов")),
                ("unit_type", models.CharField(choices=[("sqm", "Площадь (м²)"), ("linear", "Длина (м.п.)"), ("fixed", "Фиксированные пакеты")], default="sqm", max_length=16, verbose_name="Тип расчёта")),
                ("unit_label", models.CharField(default="м²", max_length=32, verbose_name="Единица измерения")),
                ("area_min", models.PositiveIntegerField(default=20, verbose_name="Мин. значение слайдера")),
                ("area_max", models.PositiveIntegerField(default=300, verbose_name="Макс. значение слайдера")),
                ("area_step", models.PositiveIntegerField(default=5, verbose_name="Шаг слайдера")),
                ("area_default", models.PositiveIntegerField(default=75, verbose_name="Значение по умолчанию")),
                ("show_service_picker", models.BooleanField(default=False, verbose_name="Квиз выбора услуги (для главной)")),
                ("submit_button_text", models.CharField(default="Зафиксировать цену", max_length=64, verbose_name="Текст кнопки отправки")),
                ("is_active", models.BooleanField(default=True, verbose_name="Активен")),
                ("sort_order", models.IntegerField(default=0, verbose_name="Порядок")),
            ],
            options={
                "verbose_name": "Калькулятор (страница)",
                "verbose_name_plural": "Калькуляторы по страницам",
                "ordering": ["sort_order", "pk"],
            },
        ),
        migrations.CreateModel(
            name="CalculatorOption",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("key", models.SlugField(max_length=48, verbose_name="Код варианта")),
                ("label", models.CharField(max_length=120, verbose_name="Название")),
                ("price_per_unit", models.PositiveIntegerField(verbose_name="Цена за единицу, ₽")),
                ("sort_order", models.IntegerField(default=0, verbose_name="Порядок")),
                ("is_active", models.BooleanField(default=True, verbose_name="Показывать")),
                ("profile", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="options", to="main.calculatorprofile", verbose_name="Калькулятор")),
            ],
            options={
                "verbose_name": "Вариант калькулятора",
                "verbose_name_plural": "Варианты калькулятора",
                "ordering": ["sort_order", "pk"],
                "unique_together": {("profile", "key")},
            },
        ),
        migrations.CreateModel(
            name="CalculatorServiceChoice",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("label", models.CharField(max_length=120, verbose_name="Название услуги")),
                ("hint", models.CharField(blank=True, max_length=160, verbose_name="Подпись")),
                ("sort_order", models.IntegerField(default=0, verbose_name="Порядок")),
                ("is_active", models.BooleanField(default=True, verbose_name="Показывать")),
                ("profile", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="service_choices", to="main.calculatorprofile", verbose_name="Калькулятор (главная)")),
                ("target_profile", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="linked_from_choices", to="main.calculatorprofile", verbose_name="Калькулятор услуги")),
            ],
            options={
                "verbose_name": "Услуга в квизе",
                "verbose_name_plural": "Услуги в квизе",
                "ordering": ["sort_order", "pk"],
            },
        ),
        migrations.RunPython(seed_profiles, migrations.RunPython.noop),
    ]
