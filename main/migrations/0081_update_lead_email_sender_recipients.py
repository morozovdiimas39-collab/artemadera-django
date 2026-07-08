from django.db import migrations


FROM_EMAIL = "ads-artemadera@ro.ru"
RECIPIENTS = "morozov.diimas39@yandex.ru\ninfo@artemadera.ru"


def update_lead_email_sender_recipients(apps, schema_editor):
    LeadEmailSettings = apps.get_model("main", "LeadEmailSettings")
    cfg, _ = LeadEmailSettings.objects.get_or_create(pk=1)
    cfg.from_email = FROM_EMAIL
    cfg.notification_emails = RECIPIENTS
    cfg.save(update_fields=["from_email", "notification_emails"])


def restore_lead_email_sender_recipients(apps, schema_editor):
    LeadEmailSettings = apps.get_model("main", "LeadEmailSettings")
    cfg, _ = LeadEmailSettings.objects.get_or_create(pk=1)
    cfg.from_email = ""
    cfg.notification_emails = "morozov.diimas39@yandex.ru\nartmoderacompany@yandex.ru"
    cfg.save(update_fields=["from_email", "notification_emails"])


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0080_leademailsettings_from_email"),
    ]

    operations = [
        migrations.RunPython(
            update_lead_email_sender_recipients,
            restore_lead_email_sender_recipients,
        ),
    ]
