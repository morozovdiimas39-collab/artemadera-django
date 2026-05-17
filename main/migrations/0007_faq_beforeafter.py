from django.db import migrations, models


def seed_faq_beforeafter(apps, schema_editor):
    FaqSection = apps.get_model("main", "FaqSection")
    FaqItem = apps.get_model("main", "FaqItem")
    BeforeAfterSection = apps.get_model("main", "BeforeAfterSection")
    BeforeAfterItem = apps.get_model("main", "BeforeAfterItem")

    FaqSection.objects.get_or_create(pk=1)
    BeforeAfterSection.objects.get_or_create(pk=1)

    faqs = [
        (
            "Можно ли шлифовать деревянный дом зимой?",
            "Да. На объекте создаём временный тепловой контур (плёнка, тепловые пушки), "
            "чтобы поддерживать нужную температуру и влажность. Так шлифовка и подготовка "
            "под покраску возможны круглый год.",
            0,
        ),
        (
            "Сколько длится шлифовка дома?",
            "Срок зависит от площади, состояния древесины и сложности геометрии. "
            "В среднем дом 100–150 м² — от нескольких дней. Точные сроки фиксируем в смете после замера.",
            1,
        ),
        (
            "Что входит в стоимость шлифовки?",
            "Подготовка поверхности, шлифовка в несколько проходов, удаление пыли, "
            "контроль качества. Дополнительно — покраска, конопатка, тёплый шов по согласованию.",
            2,
        ),
        (
            "Нужна ли покраска после шлифовки?",
            "Рекомендуем защитное покрытие: шлифовка открывает поры дерева, "
            "и без ЛКМ влага и УФ быстрее разрушают древесину. Можем выполнить покраску своей бригадой.",
            3,
        ),
        (
            "Даёте ли гарантию на работы?",
            "Да, гарантия на выполненные работы прописывается в договоре. "
            "Срок зависит от вида работ и состава — обычно до 3 лет на шлифовку.",
            4,
        ),
        (
            "Работаете ли в Москве и области?",
            "Да, выезжаем по Москве и Московской области. Стоимость выезда на замер "
            "уточняем при первом обращении.",
            5,
        ),
    ]
    for question, answer, order in faqs:
        FaqItem.objects.get_or_create(
            question=question,
            defaults={"answer": answer, "sort_order": order, "is_active": True},
        )

    comparisons = [
        (
            "Шлифовка сруба",
            "images/before.jpg",
            "images/after.jpg",
            0,
        ),
        (
            "Дом из бруса",
            "images/service-2.jpg",
            "images/service-1.jpg",
            1,
        ),
    ]
    for title, before_s, after_s, order in comparisons:
        BeforeAfterItem.objects.get_or_create(
            title=title,
            defaults={
                "before_static": before_s,
                "after_static": after_s,
                "sort_order": order,
                "is_active": True,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0006_process_contact"),
    ]

    operations = [
        migrations.CreateModel(
            name="FaqSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("badge_text", models.CharField(default="ВОПРОСЫ", max_length=64, verbose_name="Бейдж")),
                ("title_prefix", models.CharField(default="Частые", max_length=80, verbose_name="Заголовок (белая часть)")),
                ("title_highlight", models.CharField(default="вопросы", max_length=80, verbose_name="Заголовок (акцент)")),
                ("description", models.TextField(default="Ответы на популярные вопросы о шлифовке деревянных домов.", verbose_name="Описание")),
                ("is_visible", models.BooleanField(default=True, verbose_name="Показывать блок")),
            ],
            options={"verbose_name": "Блок «FAQ»", "verbose_name_plural": "Блок «FAQ»"},
        ),
        migrations.CreateModel(
            name="FaqItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("question", models.CharField(max_length=300, verbose_name="Вопрос")),
                ("answer", models.TextField(verbose_name="Ответ")),
                ("sort_order", models.IntegerField(default=0, verbose_name="Порядок")),
                ("is_active", models.BooleanField(default=True, verbose_name="Показывать")),
            ],
            options={"verbose_name": "Вопрос FAQ", "verbose_name_plural": "Вопросы FAQ", "ordering": ["sort_order", "pk"]},
        ),
        migrations.CreateModel(
            name="BeforeAfterSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("badge_text", models.CharField(default="РЕЗУЛЬТАТ", max_length=64, verbose_name="Бейдж")),
                ("title_prefix", models.CharField(default="До и", max_length=80, verbose_name="Заголовок (белая часть)")),
                ("title_highlight", models.CharField(default="после", max_length=80, verbose_name="Заголовок (акцент)")),
                ("description", models.TextField(default="Сравните состояние древесины до и после профессиональной шлифовки.", verbose_name="Описание")),
                ("is_visible", models.BooleanField(default=True, verbose_name="Показывать блок")),
            ],
            options={"verbose_name": "Блок «До / После»", "verbose_name_plural": "Блок «До / После»"},
        ),
        migrations.CreateModel(
            name="BeforeAfterItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200, verbose_name="Подпись")),
                ("before_image", models.ImageField(blank=True, null=True, upload_to="before_after/", verbose_name="Фото «До»")),
                ("after_image", models.ImageField(blank=True, null=True, upload_to="before_after/", verbose_name="Фото «После»")),
                ("before_static", models.CharField(blank=True, max_length=200, verbose_name="До (static)")),
                ("after_static", models.CharField(blank=True, max_length=200, verbose_name="После (static)")),
                ("sort_order", models.IntegerField(default=0, verbose_name="Порядок")),
                ("is_active", models.BooleanField(default=True, verbose_name="Показывать")),
            ],
            options={
                "verbose_name": "Сравнение до/после",
                "verbose_name_plural": "Сравнения до/после",
                "ordering": ["sort_order", "pk"],
            },
        ),
        migrations.RunPython(seed_faq_beforeafter, migrations.RunPython.noop),
    ]
