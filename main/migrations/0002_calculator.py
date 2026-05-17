from django.db import migrations, models


def seed_calculator(apps, schema_editor):
    CalculatorConfig = apps.get_model("main", "CalculatorConfig")
    CalculatorMaterial = apps.get_model("main", "CalculatorMaterial")
    CalculatorConfig.objects.get_or_create(
        pk=1,
        defaults={
            "area_min": 20,
            "area_max": 300,
            "area_step": 5,
            "area_default": 75,
        },
    )
    materials = [
        ("srub", "Сруб (бревенчатый)", 1200, 0),
        ("brus", "Дом из бруса", 1100, 1),
        ("kleen", "Клееный брус", 1000, 2),
        ("banya", "Баня/сауна", 1500, 3),
    ]
    for key, label, price, order in materials:
        CalculatorMaterial.objects.update_or_create(
            key=key,
            defaults={
                "label": label,
                "price_per_sqm": price,
                "sort_order": order,
                "is_active": True,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CalculatorConfig",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "area_min",
                    models.PositiveIntegerField(
                        default=20, verbose_name="Мин. площадь, м²"
                    ),
                ),
                (
                    "area_max",
                    models.PositiveIntegerField(
                        default=300, verbose_name="Макс. площадь, м²"
                    ),
                ),
                (
                    "area_step",
                    models.PositiveIntegerField(default=5, verbose_name="Шаг, м²"),
                ),
                (
                    "area_default",
                    models.PositiveIntegerField(
                        default=75, verbose_name="Площадь по умолчанию, м²"
                    ),
                ),
            ],
            options={
                "verbose_name": "Настройки калькулятора",
                "verbose_name_plural": "Настройки калькулятора",
            },
        ),
        migrations.CreateModel(
            name="CalculatorMaterial",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "key",
                    models.SlugField(
                        max_length=32,
                        unique=True,
                        verbose_name="Код (srub, brus, kleen, banya)",
                    ),
                ),
                (
                    "label",
                    models.CharField(
                        max_length=120, verbose_name="Название в калькуляторе"
                    ),
                ),
                (
                    "price_per_sqm",
                    models.PositiveIntegerField(verbose_name="Цена за м², ₽"),
                ),
                ("sort_order", models.IntegerField(default=0, verbose_name="Порядок")),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Показывать"),
                ),
            ],
            options={
                "verbose_name": "Материал калькулятора",
                "verbose_name_plural": "Материалы калькулятора",
                "ordering": ["sort_order", "pk"],
            },
        ),
        migrations.RunPython(seed_calculator, migrations.RunPython.noop),
    ]
