import os

from django.db import migrations


def fix_lead_email_recipients(apps, schema_editor):
    LeadEmailSettings = apps.get_model("main", "LeadEmailSettings")
    cfg, _ = LeadEmailSettings.objects.get_or_create(pk=1)
    cfg.notification_emails = "\n".join(
        [
            "morozov.diimas39@yandex.ru",
            "artmoderacompany@yandex.ru",
        ]
    )
    cfg.smtp_login = "artmoderacompany@yandex.ru"
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
        ("main", "0039_seed_lead_email_settings"),
    ]

    operations = [
        migrations.RunPython(fix_lead_email_recipients, migrations.RunPython.noop),
    ]
