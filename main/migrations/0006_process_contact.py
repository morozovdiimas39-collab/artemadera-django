from django.db import migrations, models


def seed_process_contact(apps, schema_editor):
    WorkProcessSection = apps.get_model("main", "WorkProcessSection")
    WorkProcessStep = apps.get_model("main", "WorkProcessStep")
    ContactSection = apps.get_model("main", "ContactSection")

    WorkProcessSection.objects.get_or_create(pk=1)

    steps = [
        (
            "01",
            "Замер и выкрас",
            "Приезжаем на объект для точных замеров и бесплатно выполняем тестовую "
            "покраску прямо на вашем доме — вы видите результат до договора.",
            0,
        ),
        (
            "02",
            "Без проживания",
            "Работаем мобильными бригадами: мастера полностью автономны и не требуют "
            "от вас жилья или условий для проживания на объекте.",
            1,
        ),
        (
            "03",
            "Честная цена",
            "Фиксированная смета в договоре не меняется в процессе — никаких скрытых "
            "доплат и неожиданных статей.",
            2,
        ),
        (
            "04",
            "Многоуровневый контроль",
            "Проверяем качество на каждом этапе, чтобы исключить дефекты и гарантировать "
            "долговечный результат.",
            3,
        ),
    ]
    for num, title, desc, order in steps:
        WorkProcessStep.objects.get_or_create(
            step_number=num,
            title=title,
            defaults={"description": desc, "sort_order": order, "is_active": True},
        )

    ContactSection.objects.get_or_create(pk=1)


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0005_reviews"),
    ]

    operations = [
        migrations.CreateModel(
            name="WorkProcessSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("badge_text", models.CharField(default="КАК МЫ РАБОТАЕМ", max_length=64, verbose_name="Бейдж")),
                ("title_prefix", models.CharField(default="Этапы", max_length=80, verbose_name="Заголовок (белая часть)")),
                ("title_highlight", models.CharField(default="нашей работы", max_length=80, verbose_name="Заголовок (акцент)")),
                ("description", models.TextField(default="Прозрачный и отлаженный процесс — от первого звонка до сдачи готового объекта.", verbose_name="Описание")),
                ("is_visible", models.BooleanField(default=True, verbose_name="Показывать блок")),
            ],
            options={"verbose_name": "Блок «Этапы работы»", "verbose_name_plural": "Блок «Этапы работы»"},
        ),
        migrations.CreateModel(
            name="WorkProcessStep",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("step_number", models.CharField(max_length=4, verbose_name="Номер (01, 02…)")),
                ("title", models.CharField(max_length=120, verbose_name="Заголовок")),
                ("description", models.TextField(verbose_name="Описание")),
                ("sort_order", models.IntegerField(default=0, verbose_name="Порядок")),
                ("is_active", models.BooleanField(default=True, verbose_name="Показывать")),
            ],
            options={"verbose_name": "Этап работы", "verbose_name_plural": "Этапы работы", "ordering": ["sort_order", "pk"]},
        ),
        migrations.CreateModel(
            name="ContactSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("badge_text", models.CharField(default="СВЯЗАТЬСЯ", max_length=64, verbose_name="Бейдж")),
                ("title_prefix", models.CharField(default="Оставьте", max_length=80, verbose_name="Заголовок (белая часть)")),
                ("title_highlight", models.CharField(default="заявку", max_length=80, verbose_name="Заголовок (акцент)")),
                ("description", models.TextField(default="Расскажите о вашем доме — перезвоним в течение 30 минут.", verbose_name="Описание")),
                ("phone", models.CharField(default="+7 (495) 005-01-45", max_length=32, verbose_name="Телефон")),
                ("phone_href", models.CharField(default="74950050145", max_length=20, verbose_name="Телефон (цифры для ссылки)")),
                ("email", models.EmailField(default="info@artemadera.ru", max_length=254, verbose_name="Email")),
                ("work_hours", models.CharField(default="Пн–Пт, 9:00–21:00", max_length=120, verbose_name="Часы работы")),
                ("address", models.CharField(blank=True, default="г. Москва, м. ВДНХ, Ярославская ул., д. 8, корп. 6, офис 220", max_length=255, verbose_name="Адрес")),
                ("submit_button_text", models.CharField(default="Отправить заявку", max_length=64, verbose_name="Текст кнопки")),
                ("privacy_note", models.CharField(default="Нажимая кнопку, вы соглашаетесь с обработкой персональных данных", max_length=255, verbose_name="Примечание под формой")),
                ("is_visible", models.BooleanField(default=True, verbose_name="Показывать блок")),
            ],
            options={"verbose_name": "Блок «Обратная связь»", "verbose_name_plural": "Блок «Обратная связь»"},
        ),
        migrations.CreateModel(
            name="ContactLead",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, verbose_name="Имя")),
                ("phone", models.CharField(max_length=32, verbose_name="Телефон")),
                ("message", models.TextField(blank=True, verbose_name="Сообщение")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Дата")),
            ],
            options={"verbose_name": "Заявка с сайта", "verbose_name_plural": "Заявки с сайта", "ordering": ["-created_at"]},
        ),
        migrations.RunPython(seed_process_contact, migrations.RunPython.noop),
    ]
