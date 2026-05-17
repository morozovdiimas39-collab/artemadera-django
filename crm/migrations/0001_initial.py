import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

from crm.services import ensure_crm_defaults


def seed_crm(apps, schema_editor):
    ensure_crm_defaults()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("main", "0011_alter_contactsection_description"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CrmLeadSource",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, verbose_name="Название")),
                ("code", models.SlugField(max_length=32, unique=True, verbose_name="Код")),
                ("sort_order", models.IntegerField(default=0, verbose_name="Порядок")),
                ("is_active", models.BooleanField(default=True, verbose_name="Активен")),
            ],
            options={
                "verbose_name": "Источник",
                "verbose_name_plural": "Источники лидов",
                "ordering": ["sort_order", "pk"],
            },
        ),
        migrations.CreateModel(
            name="CrmPipeline",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, verbose_name="Название")),
                ("slug", models.SlugField(max_length=64, unique=True, verbose_name="Код")),
                ("is_default", models.BooleanField(default=False, verbose_name="По умолчанию")),
                ("sort_order", models.IntegerField(default=0, verbose_name="Порядок")),
                ("is_active", models.BooleanField(default=True, verbose_name="Активна")),
            ],
            options={
                "verbose_name": "Воронка",
                "verbose_name_plural": "Воронки",
                "ordering": ["sort_order", "pk"],
            },
        ),
        migrations.CreateModel(
            name="CrmTag",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=64, unique=True, verbose_name="Тег")),
                ("color", models.CharField(default="#78716c", max_length=7, verbose_name="Цвет")),
            ],
            options={
                "verbose_name": "Тег",
                "verbose_name_plural": "Теги",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="CrmContact",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200, verbose_name="Имя")),
                ("phone", models.CharField(db_index=True, max_length=32, verbose_name="Телефон")),
                ("email", models.EmailField(blank=True, max_length=254, verbose_name="Email")),
                ("company_name", models.CharField(blank=True, max_length=200, verbose_name="Компания")),
                ("notes", models.TextField(blank=True, verbose_name="Заметки")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создан")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлён")),
            ],
            options={
                "verbose_name": "Контакт",
                "verbose_name_plural": "Контакты",
                "ordering": ["-updated_at"],
            },
        ),
        migrations.CreateModel(
            name="CrmStage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, verbose_name="Этап")),
                ("sort_order", models.IntegerField(default=0, verbose_name="Порядок")),
                ("color", models.CharField(default="#d97706", help_text="HEX, например #d97706", max_length=7, verbose_name="Цвет")),
                (
                    "stage_type",
                    models.CharField(
                        choices=[("open", "В работе"), ("won", "Успех"), ("lost", "Отказ")],
                        default="open",
                        max_length=8,
                        verbose_name="Тип этапа",
                    ),
                ),
                (
                    "pipeline",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="stages",
                        to="crm.crmpipeline",
                        verbose_name="Воронка",
                    ),
                ),
            ],
            options={
                "verbose_name": "Этап воронки",
                "verbose_name_plural": "Этапы воронки",
                "ordering": ["pipeline", "sort_order", "pk"],
                "unique_together": {("pipeline", "name")},
            },
        ),
        migrations.CreateModel(
            name="CrmDeal",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255, verbose_name="Название сделки")),
                (
                    "amount",
                    models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name="Бюджет, ₽"),
                ),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
                (
                    "priority",
                    models.CharField(
                        choices=[("low", "Низкий"), ("normal", "Обычный"), ("high", "Высокий")],
                        default="normal",
                        max_length=8,
                        verbose_name="Приоритет",
                    ),
                ),
                ("lost_reason", models.CharField(blank=True, max_length=255, verbose_name="Причина отказа")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создана")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлена")),
                ("closed_at", models.DateTimeField(blank=True, null=True, verbose_name="Закрыта")),
                (
                    "contact",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="deals",
                        to="crm.crmcontact",
                        verbose_name="Контакт",
                    ),
                ),
                (
                    "pipeline",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="deals",
                        to="crm.crmpipeline",
                        verbose_name="Воронка",
                    ),
                ),
                (
                    "responsible",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="crm_deals",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Ответственный",
                    ),
                ),
                (
                    "source",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="deals",
                        to="crm.crmleadsource",
                        verbose_name="Источник",
                    ),
                ),
                (
                    "stage",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="deals",
                        to="crm.crmstage",
                        verbose_name="Этап",
                    ),
                ),
                (
                    "site_lead",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="crm_deal",
                        to="main.contactlead",
                        verbose_name="Заявка с сайта",
                    ),
                ),
                ("tags", models.ManyToManyField(blank=True, related_name="deals", to="crm.crmtag", verbose_name="Теги")),
            ],
            options={
                "verbose_name": "Сделка",
                "verbose_name_plural": "Сделки",
                "ordering": ["-updated_at"],
            },
        ),
        migrations.CreateModel(
            name="CrmTask",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255, verbose_name="Задача")),
                ("due_at", models.DateTimeField(blank=True, null=True, verbose_name="Срок")),
                ("is_done", models.BooleanField(default=False, verbose_name="Выполнена")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создана")),
                ("completed_at", models.DateTimeField(blank=True, null=True, verbose_name="Завершена")),
                (
                    "assigned_to",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="crm_tasks",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Исполнитель",
                    ),
                ),
                (
                    "deal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tasks",
                        to="crm.crmdeal",
                        verbose_name="Сделка",
                    ),
                ),
            ],
            options={
                "verbose_name": "Задача",
                "verbose_name_plural": "Задачи",
                "ordering": ["is_done", "due_at", "-created_at"],
            },
        ),
        migrations.CreateModel(
            name="CrmActivity",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "activity_type",
                    models.CharField(
                        choices=[
                            ("note", "Заметка"),
                            ("call", "Звонок"),
                            ("meeting", "Встреча"),
                            ("email", "Письмо"),
                            ("stage_change", "Смена этапа"),
                            ("created", "Создание"),
                        ],
                        default="note",
                        max_length=16,
                        verbose_name="Тип",
                    ),
                ),
                ("body", models.TextField(verbose_name="Текст")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Дата")),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="crm_activities",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Автор",
                    ),
                ),
                (
                    "deal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="activities",
                        to="crm.crmdeal",
                        verbose_name="Сделка",
                    ),
                ),
            ],
            options={
                "verbose_name": "Активность",
                "verbose_name_plural": "Активности",
                "ordering": ["-created_at"],
            },
        ),
        migrations.RunPython(seed_crm, migrations.RunPython.noop),
    ]
