from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ContactLead
from .image_optimization import optimize_instance_images


@receiver(post_save, sender=ContactLead, dispatch_uid="main_contact_lead_email_notify")
def contact_lead_send_notification(sender, instance, created, **kwargs):
    if not created:
        return
    from .lead_notifications import send_lead_created_email

    send_lead_created_email(instance)


@receiver(post_save, dispatch_uid="main_optimize_uploaded_images")
def optimize_uploaded_images(sender, instance, created, **kwargs):
    if getattr(sender._meta, "app_label", "") != "main":
        return
    if sender is ContactLead:
        return
    optimize_instance_images(instance)
