import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ContactLead

logger = logging.getLogger(__name__)


@receiver(post_save, sender=ContactLead, dispatch_uid="main_contact_lead_process")
def contact_lead_process(sender, instance, created, **kwargs):
    """Создаёт сделку CRM и отправляет уведомление, не ломая сохранение заявки."""
    if not created:
        return

    from crm.services import create_deal_from_site_lead

    try:
        create_deal_from_site_lead(instance)
    except Exception:
        logger.exception("Не удалось создать сделку CRM для заявки #%s", instance.pk)

    try:
        from .lead_notifications import send_lead_created_email

        send_lead_created_email(instance)
    except Exception:
        logger.exception("Не удалось отправить email для заявки #%s", instance.pk)
