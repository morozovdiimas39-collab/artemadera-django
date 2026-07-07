from django.db import migrations, models


def mark_unconfirmed_leads_pending(apps, schema_editor):
    ContactLead = apps.get_model("main", "ContactLead")
    ContactLead.objects.filter(
        direct_status="IN_PROGRESS",
        direct_status_updated_at__isnull=True,
    ).update(direct_status="PENDING")


def restore_pending_as_in_progress(apps, schema_editor):
    ContactLead = apps.get_model("main", "ContactLead")
    ContactLead.objects.filter(direct_status="PENDING").update(direct_status="IN_PROGRESS")


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0055_apply_screenshot_service_edits"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contactlead",
            name="direct_status",
            field=models.CharField(
                choices=[
                    ("PENDING", "Не отмечено"),
                    ("IN_PROGRESS", "Целевой"),
                    ("PAID", "Оплачен"),
                    ("CANCELLED", "Нецелевой"),
                    ("SPAM", "Спам"),
                ],
                default="PENDING",
                help_text=(
                    "Новая заявка не попадает в CSV, пока её не отметили из письма: "
                    "целевой, нецелевой, спам, оплачен."
                ),
                max_length=16,
                verbose_name="Статус для CSV Директа",
            ),
        ),
        migrations.RunPython(mark_unconfirmed_leads_pending, restore_pending_as_in_progress),
    ]
