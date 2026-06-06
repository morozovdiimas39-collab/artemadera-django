import os

from django.db import migrations


OWNER_EMAIL = "morozov.diimas39@yandex.ru"


def restore_owner_email_sender(apps, schema_editor):
    LeadEmailSettings = apps.get_model("main", "LeadEmailSettings")
    cfg, _ = LeadEmailSettings.objects.get_or_create(pk=1)
    cfg.smtp_login = OWNER_EMAIL

    env_login = (
        os.environ.get("EMAIL_HOST_USER")
        or os.environ.get("EMAIL_LOGIN")
        or os.environ.get("SMTP_LOGIN")
        or ""
    ).strip().lower()
    if env_login == OWNER_EMAIL:
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
        ("main", "0047_use_artmodera_company_sender"),
    ]

    operations = [
        migrations.RunPython(restore_owner_email_sender, migrations.RunPython.noop),
    ]
