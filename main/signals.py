from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ContactLead


@receiver(post_save, sender=ContactLead, dispatch_uid="main_contact_lead_email_notify")
def contact_lead_send_notification(sender, instance, created, **kwargs):
    if not created:
        return
    from .lead_notifications import send_lead_created_email

    send_lead_created_email(instance)

