import os

from django.db import migrations


def restore_working_sender_two_recipients(apps, schema_editor):
    LeadEmailSettings = apps.get_model("main", "LeadEmailSettings")
    cfg, _ = LeadEmailSettings.objects.get_or_create(pk=1)
    cfg.notification_emails = "\n".join(
        [
            "morozov.diimas39@yandex.ru",
            "artmoderacompany@yandex.ru",
        ]
    )
    cfg.smtp_login = (
        os.environ.get("EMAIL_HOST_USER")
        or os.environ.get("EMAIL_LOGIN")
        or os.environ.get("SMTP_LOGIN")
        or "morozov.diimas39@yandex.ru"
    )
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
        ("main", "0040_fix_lead_email_recipients"),
    ]

    operations = [
        migrations.RunPython(restore_working_sender_two_recipients, migrations.RunPython.noop),
    ]
