"""
CSV для «Загрузка конверсий по ссылке» (Яндекс.Директ / Метрика).

Спецификация колонок: docs/DIRECT_CONVERSIONS_CSV_SPEC.md
Справка: https://yandex.ru/support/direct/statistics/conversions.html

Данные: сделки CRM (CrmDeal) и заявки с сайта без сделки (ContactLead).
URL: GET /export/yandex-direct-conversions.csv?token=<DIRECT_CONVERSIONS_CSV_TOKEN>
"""
from __future__ import annotations

import csv
import hashlib
import re
from datetime import timedelta
from io import StringIO
from typing import Any, Iterator

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed
from django.utils import timezone

from crm.models import CrmDeal, CrmStage
from main.models import ContactLead

# Окно атрибуции: старше 113 дней Директ отклонит
MAX_DAYS_AGE = 113

BLOCKLIST_PHONES_NORMALIZED = {
    "71231312312",
    "72831612312",
    "72424234234",
    "78937249567",
    "78987969650",
    "78985584601",
    "78922192054",
    "78942776924",
    "78971024149",
    "78941728295",
    "78907377733",
    "78986017110",
    "78922116314",
    "78903471767",
    "78955006792",
    "72283161248",
}

MAX_REVENUE = 9223372036854
REVENUE_OPEN = 300
REVENUE_WON = 15000


def _lead_is_marked_for_direct(lead: ContactLead) -> bool:
    status = (getattr(lead, "direct_status", "") or "").strip()
    return bool(getattr(lead, "direct_status_updated_at", None)) and status != ContactLead.DIRECT_STATUS_PENDING


def _lead_status_revenue(lead: ContactLead) -> tuple[str, int] | None:
    if not _lead_is_marked_for_direct(lead):
        return None
    status = (getattr(lead, "direct_status", "") or ContactLead.DIRECT_STATUS_PENDING).strip()
    if status == ContactLead.DIRECT_STATUS_PAID:
        return "PAID", REVENUE_WON
    if status == ContactLead.DIRECT_STATUS_CANCELLED:
        return "CANCELLED", 0
    if status == ContactLead.DIRECT_STATUS_SPAM:
        return "SPAM", 0
    return "IN_PROGRESS", REVENUE_OPEN


def _normalize_phone(phone: str) -> str:
    """Телефон: только цифры, код страны, 11 знаков с 7 для РФ."""
    if not phone:
        return ""
    digits = re.sub(r"\D", "", str(phone))
    if len(digits) == 10 and digits.startswith("9"):
        digits = "7" + digits
    elif len(digits) == 11 and digits.startswith("8"):
        digits = "7" + digits[1:]
    if len(digits) < 10:
        return ""
    return digits


def _phone_md5(normalized_phone: str) -> str:
    if not normalized_phone:
        return ""
    return hashlib.md5(normalized_phone.encode("utf-8")).hexdigest().lower()


def _valid_client_id(raw: str) -> str:
    """ClientID Метрики: только положительное целое число."""
    if not raw:
        return ""
    s = str(raw).strip()
    if s.lower().startswith("telegram_"):
        return ""
    if s.isdigit() and int(s) > 0:
        return s
    return ""


def _format_direct_datetime(dt) -> str:
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt, timezone.get_current_timezone())
    local = timezone.localtime(dt)
    return local.strftime("%d.%m.%Y %H:%M:%S")


def _deal_status_revenue(deal: CrmDeal) -> tuple[str, int]:
    if getattr(deal, "site_lead_id", None):
        status_revenue = _lead_status_revenue(deal.site_lead)
        if status_revenue is None:
            return "", 0
        return status_revenue

    st = deal.stage.stage_type
    if st == CrmStage.TYPE_WON:
        return "PAID", REVENUE_WON
    if st == CrmStage.TYPE_LOST:
        reason = (deal.lost_reason or "").lower()
        if any(x in reason for x in ("спам", "нецелев", "не целев")):
            return "SPAM", 0
        return "CANCELLED", 0
    return "IN_PROGRESS", REVENUE_OPEN


def _iter_rows() -> Iterator[list[Any]]:
    now = timezone.now()
    cutoff = now - timedelta(days=MAX_DAYS_AGE)

    deals = (
        CrmDeal.objects.select_related("contact", "stage", "site_lead")
        .filter(contact__isnull=False)
        .exclude(contact__phone="")
        .order_by("-updated_at")
    )

    for deal in deals:
        dt = deal.updated_at
        if dt > now:
            dt = now
        if dt < cutoff:
            continue

        phone = _normalize_phone(deal.contact.phone)
        if not phone:
            continue
        if phone in BLOCKLIST_PHONES_NORMALIZED:
            continue

        ym = ""
        if deal.site_lead_id:
            ym = _valid_client_id((deal.site_lead.ym_client_id or "").strip())

        if not ym and not phone:
            continue

        order_status, revenue_val = _deal_status_revenue(deal)
        if not order_status:
            continue
        if revenue_val < 0 or revenue_val > MAX_REVENUE:
            revenue_val = 0
        revenue = f"{float(revenue_val):.1f}" if revenue_val else ""

        yield [
            _format_direct_datetime(dt),
            str(deal.pk),
            f"deal_{deal.pk}",
            ym,
            "",
            phone,
            "",
            _phone_md5(phone),
            order_status,
            revenue,
            "",
        ]

    orphans = (
        ContactLead.objects.filter(crm_deal__isnull=True)
        .exclude(phone="")
        .order_by("-created_at")
    )
    for lead in orphans:
        dt = lead.created_at
        if dt > now:
            dt = now
        if dt < cutoff:
            continue

        phone = _normalize_phone(lead.phone)
        if not phone or phone in BLOCKLIST_PHONES_NORMALIZED:
            continue

        ym = _valid_client_id(lead.ym_client_id or "")
        if not ym and not phone:
            continue

        status_revenue = _lead_status_revenue(lead)
        if status_revenue is None:
            continue
        order_status, revenue_val = status_revenue
        revenue = f"{float(revenue_val):.1f}" if revenue_val else ""

        yield [
            _format_direct_datetime(dt),
            str(lead.pk),
            f"lead_{lead.pk}",
            ym,
            "",
            phone,
            "",
            _phone_md5(phone),
            order_status,
            revenue,
            "",
        ]


def build_direct_conversions_csv() -> str:
    buf = StringIO()
    writer = csv.writer(buf, delimiter=";", quoting=csv.QUOTE_MINIMAL)
    writer.writerow(
        [
            "create_date_time",
            "id",
            "client_uniq_id",
            "client_ids",
            "emails",
            "phones",
            "emails_md5",
            "phones_md5",
            "order_status",
            "revenue",
            "cost",
        ]
    )
    for row in _iter_rows():
        writer.writerow(row)
    data = buf.getvalue()
    buf.close()
    return data


def direct_conversions_csv_view(request):
    """View: отдаёт CSV для загрузки конверсий в Директ."""
    if request.method == "OPTIONS":
        return HttpResponse(
            "",
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Max-Age": "86400",
            },
        )

    if request.method != "GET":
        return HttpResponseNotAllowed(["GET", "OPTIONS"])

    expected = getattr(settings, "DIRECT_CONVERSIONS_CSV_TOKEN", "") or ""
    if not expected:
        return HttpResponseForbidden("Нужен непустой DIRECT_CONVERSIONS_CSV_TOKEN (см. .env или env сервера).")
    if request.GET.get("token") != expected:
        return HttpResponseForbidden("Invalid token")

    csv_content = build_direct_conversions_csv()
    return HttpResponse(
        csv_content,
        content_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": 'attachment; filename="direct_conversions.csv"',
            "Access-Control-Allow-Origin": "*",
            "Cache-Control": "no-cache, max-age=0",
        },
    )
