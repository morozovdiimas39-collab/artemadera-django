from django.db import migrations, models


def create_lead_email_settings_row(apps, schema_editor):
    LeadEmailSettings = apps.get_model("main", "LeadEmailSettings")
    LeadEmailSettings.objects.get_or_create(pk=1)


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0029_shlifovka_services_from_admin"),
    ]

    operations = [
        migrations.CreateModel(
            name="LeadEmailSettings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "notification_emails",
                    models.TextField(
                        blank=True,
                        help_text=(
                            "Один или несколько адресов — через запятую или с новой строки. "
                            "Пока поле пустое, письма не отправляются. Настройка SMTP — в переменных окружения сервера."
                        ),
                        verbose_name="Email для уведомлений",
                    ),
                ),
            ],
            options={
                "verbose_name": "Уведомления о заявках (email)",
                "verbose_name_plural": "Уведомления о заявках (email)",
            },
        ),
        migrations.RunPython(create_lead_email_settings_row, migrations.RunPython.noop),
    ]
