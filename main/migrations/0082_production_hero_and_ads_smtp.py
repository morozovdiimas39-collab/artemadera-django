from django.db import migrations


PRODUCTION_HERO = "pages/hero/56bc28f1-9fc0-42e1-b0c8-917d3fe4c1ad.webp"

SMTP_LOGIN = "ads-artemadera@ro.ru"
SMTP_HOST = "smtp.rambler.ru"
SMTP_PORT = 465
FROM_EMAIL = "ads-artemadera@ro.ru"
RECIPIENTS = "morozov.diimas39@yandex.ru\ninfo@artemadera.ru"


def apply_changes(apps, schema_editor):
    SitePage = apps.get_model("main", "SitePage")
    LeadEmailSettings = apps.get_model("main", "LeadEmailSettings")

    SitePage.objects.filter(page_key="proizvodstvo").update(
        hero_image=PRODUCTION_HERO,
        hero_static_image="",
    )

    cfg, _ = LeadEmailSettings.objects.get_or_create(pk=1)
    cfg.smtp_login = SMTP_LOGIN
    cfg.from_email = FROM_EMAIL
    cfg.notification_emails = RECIPIENTS
    cfg.smtp_host = SMTP_HOST
    cfg.smtp_port = SMTP_PORT
    cfg.smtp_use_tls = False
    cfg.smtp_use_ssl = True
    cfg.save(
        update_fields=[
            "smtp_login",
            "from_email",
            "notification_emails",
            "smtp_host",
            "smtp_port",
            "smtp_use_tls",
            "smtp_use_ssl",
        ]
    )


def restore_changes(apps, schema_editor):
    SitePage = apps.get_model("main", "SitePage")
    LeadEmailSettings = apps.get_model("main", "LeadEmailSettings")

    SitePage.objects.filter(page_key="proizvodstvo").update(
        hero_image="",
        hero_static_image="images/hero-bg.jpg",
    )

    cfg, _ = LeadEmailSettings.objects.get_or_create(pk=1)
    cfg.smtp_login = "morozov.diimas39@yandex.ru"
    cfg.from_email = "ads-artemadera@ro.ru"
    cfg.notification_emails = RECIPIENTS
    cfg.smtp_host = "smtp.yandex.ru"
    cfg.smtp_port = 587
    cfg.smtp_use_tls = True
    cfg.smtp_use_ssl = False
    cfg.save(
        update_fields=[
            "smtp_login",
            "from_email",
            "notification_emails",
            "smtp_host",
            "smtp_port",
            "smtp_use_tls",
            "smtp_use_ssl",
        ]
    )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0081_update_lead_email_sender_recipients"),
    ]

    operations = [
        migrations.RunPython(apply_changes, restore_changes),
    ]
