import logging
from threading import Thread

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ContactLead

logger = logging.getLogger(__name__)


def _send_lead_notification_in_background(lead_id):
    from django.db import close_old_connections

    close_old_connections()
    try:
        lead = ContactLead.objects.get(pk=lead_id)
        from .lead_notifications import send_lead_created_email

        send_lead_created_email(lead)
    except Exception:
        logger.exception("Не удалось отправить email для заявки #%s", lead_id)
    finally:
        close_old_connections()


@receiver(post_save, sender=ContactLead, dispatch_uid="main_contact_lead_process")
def contact_lead_process(sender, instance, created, **kwargs):
    """Сначала сохраняет заявку в CRM, затем отправляет email независимо от ответа формы."""
    if not created:
        return

    from crm.services import create_deal_from_site_lead

    try:
        create_deal_from_site_lead(instance)
    except Exception:
        logger.exception("Не удалось создать сделку CRM для заявки #%s", instance.pk)

    Thread(
        target=_send_lead_notification_in_background,
        args=(instance.pk,),
        name=f"lead-email-{instance.pk}",
        daemon=True,
    ).start()
