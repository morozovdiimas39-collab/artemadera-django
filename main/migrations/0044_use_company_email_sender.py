import os

from django.db import migrations, models


COMPANY_EMAIL = "artmoderacompany@yandex.ru"


def use_company_email_sender(apps, schema_editor):
    LeadEmailSettings = apps.get_model("main", "LeadEmailSettings")
    cfg, _ = LeadEmailSettings.objects.get_or_create(pk=1)
    cfg.smtp_login = COMPANY_EMAIL

    env_login = (
        os.environ.get("EMAIL_HOST_USER")
        or os.environ.get("EMAIL_LOGIN")
        or os.environ.get("SMTP_LOGIN")
        or ""
    ).strip().lower()
    if env_login == COMPANY_EMAIL:
        cfg.smtp_password = (
            os.environ.get("EMAIL_HOST_PASSWORD")
            or os.environ.get("EMAIL_PASSWORD")
            or os.environ.get("SMTP_PASSWORD")
            or cfg.smtp_password
        )

    cfg.smtp_host = "smtp.yandex.ru"
    cfg.smtp_port = 587
    cfg.smtp_use_tls = True
    cfg.smtp_use_ssl = False
    cfg.save()


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0043_apply_codex_document_updates"),
    ]

    operations = [
        migrations.RunPython(use_company_email_sender, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="leademailsettings",
            name="smtp_login",
            field=models.EmailField(
                blank=True,
                help_text="Корпоративная почта, от имени которой отправляются уведомления. Если пусто — берётся EMAIL_HOST_USER из окружения.",
                max_length=254,
                verbose_name="Логин SMTP",
            ),
        ),
    ]
