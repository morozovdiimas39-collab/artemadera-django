from django.db.models.signals import post_migrate, post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from .models import CrmActivity, CrmDeal, CrmStage
from .services import ensure_crm_defaults, log_stage_change


@receiver(post_migrate)
def seed_crm_on_migrate(sender, **kwargs):
    if sender.name != "crm":
        return
    ensure_crm_defaults()


@receiver(pre_save, sender=CrmDeal)
def deal_capture_old_stage(sender, instance, **kwargs):
    if not instance.pk:
        instance._old_stage_id = None
        return
    instance._old_stage_id = (
        CrmDeal.objects.filter(pk=instance.pk).values_list("stage_id", flat=True).first()
    )


@receiver(post_save, sender=CrmDeal)
def deal_after_save(sender, instance, created, **kwargs):
    if created:
        body = (
            "Сделка создана из заявки на сайте."
            if instance.site_lead_id
            else "Сделка создана."
        )
        CrmActivity.objects.create(
            deal=instance,
            activity_type=CrmActivity.TYPE_CREATED,
            body=body,
            author=getattr(instance, "_stage_change_user", None),
        )
        return

    old_stage_id = getattr(instance, "_old_stage_id", None)
    if old_stage_id is None or old_stage_id == instance.stage_id:
        return

    old_stage = CrmStage.objects.filter(pk=old_stage_id).first()
    new_stage = instance.stage
    if not old_stage or not new_stage:
        return

    if new_stage.stage_type in (CrmStage.TYPE_WON, CrmStage.TYPE_LOST):
        if not instance.closed_at:
            CrmDeal.objects.filter(pk=instance.pk).update(closed_at=timezone.now())
    elif old_stage.stage_type in (CrmStage.TYPE_WON, CrmStage.TYPE_LOST):
        CrmDeal.objects.filter(pk=instance.pk).update(closed_at=None)

    log_stage_change(
        instance,
        old_stage,
        new_stage,
        user=getattr(instance, "_stage_change_user", None),
        note=getattr(instance, "_stage_change_note", ""),
    )
