from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db import transaction

from .models import (
    CrmActivity,
    CrmContact,
    CrmDeal,
    CrmLeadSource,
    CrmPipeline,
    CrmStage,
)

User = get_user_model()

DEFAULT_PIPELINE = {
    "name": "Продажи",
    "slug": "sales",
    "stages": [
        ("Новая заявка", "#78716c", CrmStage.TYPE_OPEN, 10),
        ("Первый контакт", "#3b82f6", CrmStage.TYPE_OPEN, 20),
        ("Замер назначен", "#8b5cf6", CrmStage.TYPE_OPEN, 30),
        ("Смета отправлена", "#f59e0b", CrmStage.TYPE_OPEN, 40),
        ("Договор", "#10b981", CrmStage.TYPE_OPEN, 50),
        ("Успешно", "#22c55e", CrmStage.TYPE_WON, 60),
        ("Отказ", "#ef4444", CrmStage.TYPE_LOST, 70),
    ],
}

DEFAULT_SOURCES = [
    ("Сайт — контакты", "website_contact"),
    ("Сайт — замер", "website_measure"),
    ("Звонок", "phone"),
    ("Рекомендация", "referral"),
    ("Вручную", "manual"),
]


def ensure_crm_defaults():
    """Создаёт воронку, этапы и источники, если их ещё нет."""
    pipeline, _ = CrmPipeline.objects.get_or_create(
        slug=DEFAULT_PIPELINE["slug"],
        defaults={
            "name": DEFAULT_PIPELINE["name"],
            "is_default": True,
            "sort_order": 0,
        },
    )
    if not pipeline.is_default:
        pipeline.is_default = True
        pipeline.save(update_fields=["is_default"])

    for name, color, stage_type, order in DEFAULT_PIPELINE["stages"]:
        CrmStage.objects.get_or_create(
            pipeline=pipeline,
            name=name,
            defaults={
                "color": color,
                "stage_type": stage_type,
                "sort_order": order,
            },
        )

    for name, code in DEFAULT_SOURCES:
        CrmLeadSource.objects.get_or_create(
            code=code,
            defaults={"name": name, "sort_order": 0},
        )

    return pipeline


def get_default_pipeline() -> CrmPipeline:
    pipeline = CrmPipeline.objects.filter(is_default=True, is_active=True).first()
    if pipeline:
        return pipeline
    return ensure_crm_defaults()


def get_initial_stage(pipeline: CrmPipeline) -> CrmStage:
    stage = (
        pipeline.stages.filter(stage_type=CrmStage.TYPE_OPEN).order_by("sort_order").first()
    )
    if stage:
        return stage
    return pipeline.stages.order_by("sort_order").first()


def get_source(code: str) -> CrmLeadSource | None:
    return CrmLeadSource.objects.filter(code=code, is_active=True).first()


def normalize_phone(phone: str) -> str:
    return "".join(ch for ch in phone if ch.isdigit() or ch == "+")


def get_or_create_contact(*, name: str, phone: str, email: str = "") -> CrmContact:
    phone_norm = normalize_phone(phone)
    contact = CrmContact.objects.filter(phone=phone).first()
    if contact:
        updated = []
        if name and name != "—" and contact.name in ("", "—", phone):
            contact.name = name
            updated.append("name")
        if email and not contact.email:
            contact.email = email
            updated.append("email")
        if updated:
            contact.save(update_fields=updated + ["updated_at"])
        return contact

    display_name = name if name and name != "—" else phone
    return CrmContact.objects.create(
        name=display_name,
        phone=phone,
        email=email or "",
    )


def log_stage_change(deal, old_stage, new_stage, *, user=None, note=""):
    parts = [f"Этап: {old_stage.name} → {new_stage.name}"]
    if note:
        parts.append(note)
    CrmActivity.objects.create(
        deal=deal,
        activity_type=CrmActivity.TYPE_STAGE,
        body="\n".join(parts),
        author=user,
    )


def _lead_traffic_lines(lead) -> list[str]:
    labels = [
        ("page_url", "Страница заявки"),
        ("landing_page", "Посадочная страница"),
        ("referrer", "Referrer"),
        ("utm_source", "utm_source"),
        ("utm_medium", "utm_medium"),
        ("utm_campaign", "utm_campaign"),
        ("utm_content", "utm_content"),
        ("utm_term", "utm_term"),
        ("yclid", "yclid"),
        ("gclid", "gclid"),
        ("fbclid", "fbclid"),
        ("ymclid", "ymclid"),
        ("ym_client_id", "ClientID Метрики"),
    ]
    lines = []
    for attr, label in labels:
        value = (getattr(lead, attr, "") or "").strip()
        if value:
            lines.append(f"{label}: {value}")
    return lines


@transaction.atomic
def create_deal_from_site_lead(lead, *, from_block: str | None = None, user=None) -> CrmDeal:
    """Создаёт контакт и сделку из заявки ContactLead."""
    existing_deal = CrmDeal.objects.filter(site_lead=lead).first()
    if existing_deal:
        return existing_deal

    ensure_crm_defaults()
    pipeline = get_default_pipeline()
    stage = get_initial_stage(pipeline)

    if from_block == "measure":
        source = get_source("website_measure")
        title = f"Замер — {lead.phone}"
    else:
        source = get_source("website_contact")
        title = f"Заявка — {lead.phone}"

    contact = get_or_create_contact(name=lead.name, phone=lead.phone)
    description_parts = []
    if lead.message:
        description_parts.append(lead.message)
    if from_block:
        description_parts.append(f"Блок формы: {from_block}")
    traffic_lines = _lead_traffic_lines(lead)
    if traffic_lines:
        description_parts.append("Источник заявки:\n" + "\n".join(traffic_lines))

    deal = CrmDeal.objects.create(
        title=title,
        contact=contact,
        pipeline=pipeline,
        stage=stage,
        source=source,
        description="\n\n".join(description_parts),
        site_lead=lead,
        responsible=user,
    )

    activity_body = "\n\n".join(part for part in [lead.message, "\n".join(traffic_lines)] if part)
    if activity_body:
        CrmActivity.objects.create(
            deal=deal,
            activity_type=CrmActivity.TYPE_NOTE,
            body=activity_body,
            author=user,
        )

    return deal
