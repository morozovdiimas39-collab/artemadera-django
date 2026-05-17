from django.db import migrations


def ensure_profiles(apps, schema_editor):
    """Ensure all service calculator profiles exist with correct options.
    Safe to run multiple times — uses update_or_create."""
    CalculatorProfile = apps.get_model("main", "CalculatorProfile")
    CalculatorOption = apps.get_model("main", "CalculatorOption")

    def upsert(slug, **fields):
        profile, _ = CalculatorProfile.objects.update_or_create(
            slug=slug, defaults={**{"is_active": True}, **fields}
        )
        return profile

    def opt(profile, key, label, price, order=0):
        CalculatorOption.objects.update_or_create(
            profile=profile,
            key=key,
            defaults={"label": label, "price_per_unit": price, "sort_order": order, "is_active": True},
        )

    pokraska = upsert(
        "pokraska",
        name="Покраска",
        title="Калькулятор покраски",
        description="Узнайте примерную стоимость покраски деревянного дома. Точную смету — после замера.",
        options_label="Тип покрытия",
        unit_type="sqm",
        unit_label="м²",
        sort_order=1,
    )
    for key, label, price, order in [
        ("oil", "Масло (Osmo, Remmers)", 650, 0),
        ("lazur", "Лазурь (Caparol, Belinka)", 750, 1),
        ("antisept", "Антисептик + грунт", 550, 2),
        ("complex", "Комплекс (2 слоя)", 1100, 3),
    ]:
        opt(pokraska, key, label, price, order)

    teplyy = upsert(
        "teplyy-shov",
        name="Тёплый шов",
        title="Калькулятор тёплого шва",
        description="Расчёт стоимости герметизации межвенцовых швов по погонным метрам.",
        options_label="Тип герметизации",
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
        ("konopatka", "Конопатка (восстановление)", 250, 2),
    ]:
        opt(teplyy, key, label, price, order)

    obsada = upsert(
        "obsada",
        name="Обсада",
        title="Калькулятор обсады",
        description="Ориентировочная стоимость окосячки окон и дверей. Точно — после замера проёмов.",
        options_label="Тип проёма",
        unit_type="fixed",
        unit_label="",
        area_min=1,
        area_max=1,
        area_default=1,
        sort_order=3,
    )
    for key, label, price, order in [
        ("okosyachka", "Обсада / окосячка (весь дом)", 85000, 0),
        ("okna", "Обсада окна (1 шт)", 12000, 1),
        ("dveri", "Обсада двери (1 шт)", 15000, 2),
        ("arki", "Обсада арки (1 шт)", 18000, 3),
    ]:
        opt(obsada, key, label, price, order)

    kryshi = upsert(
        "kryshi",
        name="Крыши",
        title="Калькулятор кровельных работ",
        description="Примерная стоимость монтажа или ремонта кровли. Точная цена — после выезда на объект.",
        options_label="Тип кровли",
        unit_type="sqm",
        unit_label="м²",
        sort_order=4,
    )
    for key, label, price, order in [
        ("metall", "Металлочерепица", 1800, 0),
        ("gibkaya", "Гибкая черепица", 2200, 1),
        ("faltsevaya", "Фальцевая кровля", 2800, 2),
        ("remont", "Ремонт кровли", 1200, 3),
    ]:
        opt(kryshi, key, label, price, order)

    injeneriya = upsert(
        "injeneriya",
        name="Инженерия",
        title="Калькулятор инженерных работ",
        description="Ориентировочная стоимость инженерных систем. Точная смета — после проектирования.",
        options_label="Комплектация",
        unit_type="fixed",
        unit_label="",
        area_min=1,
        area_max=1,
        area_default=1,
        sort_order=5,
    )
    for key, label, price, order in [
        ("project", "Проект инженерии", 45000, 0),
        ("electro", "Электрика (монтаж)", 85000, 1),
        ("voda", "Водоснабжение (монтаж)", 95000, 2),
        ("otoplenie", "Отопление (монтаж)", 145000, 3),
        ("complex", "Инженерия под ключ", 320000, 4),
    ]:
        opt(injeneriya, key, label, price, order)


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0012_calculator_profiles"),
    ]

    operations = [
        migrations.RunPython(ensure_profiles, migrations.RunPython.noop),
    ]
