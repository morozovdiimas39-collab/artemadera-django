import logging

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .image_optimization import optimize_instance_images
from .models import (
    BeforeAfterSection,
    BlogPost,
    ContactLead,
    ExperienceSection,
    HomeQuizSettings,
    PortfolioProject,
    PortfolioProjectImage,
    Review,
    Service,
    SitePage,
    WorkProcessSection,
)

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


IMAGE_MODELS = (
    HomeQuizSettings,
    Service,
    SitePage,
    PortfolioProject,
    PortfolioProjectImage,
    ExperienceSection,
    Review,
    WorkProcessSection,
    BeforeAfterSection,
    BlogPost,
)


def _has_uploaded_images(instance):
    for field in instance._meta.fields:
        if not isinstance(field, models.ImageField):
            continue
        field_file = getattr(instance, field.name, None)
        if field_file and getattr(field_file, "name", ""):
            return True
    return False


for image_model in IMAGE_MODELS:
    @receiver(post_save, sender=image_model, dispatch_uid=f"main_optimize_images_{image_model.__name__}")
    def optimize_uploaded_images(sender, instance, **kwargs):
        if not _has_uploaded_images(instance):
            return
        try:
            optimize_instance_images(instance)
        except Exception:
            logger.exception(
                "Не удалось оптимизировать изображения %s #%s",
                sender.__name__,
                instance.pk,
            )
