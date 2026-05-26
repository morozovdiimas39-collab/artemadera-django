"""Письма при новых заявках с сайта (ContactLead)."""
from __future__ import annotations

import logging
import re

from django.conf import settings
from django.core.mail import get_connection, send_mail

logger = logging.getLogger(__name__)


def parse_notification_emails(raw: str) -> list[str]:
    if not raw or not str(raw).strip():
        return []
    parts = re.split(r"[\s,;]+", str(raw).strip())
    out: list[str] = []
    for p in parts:
        s = p.strip()
        if s and "@" in s:
            out.append(s)
    seen: set[str] = set()
    uniq: list[str] = []
    for e in out:
        key = e.lower()
        if key not in seen:
            seen.add(key)
            uniq.append(e)
    return uniq


def send_lead_created_email(lead) -> None:
    """Отправляет письмо о новой заявке, если в админке заданы адреса."""
    from .models import LeadEmailSettings

    try:
        cfg = LeadEmailSettings.load()
    except Exception:
        logger.exception("LeadEmailSettings.load failed — миграции применены? (main.0030)")
        return

    raw = (cfg.notification_emails or "").strip()
    if not raw:
        logger.warning(
            "Письмо о заявке #%s не отправлено: в админке «Почта: уведомления о заявках» "
            "пустое поле «Email для уведомлений».",
            getattr(lead, "pk", "?"),
        )
        return

    recipients = parse_notification_emails(raw)
    if not recipients:
        logger.warning(
            "Письмо о заявке #%s не отправлено: в настройках указан текст без валидных email.",
            getattr(lead, "pk", "?"),
        )
        return

    subject = f"Новая заявка с сайта: {lead.name} — {lead.phone}"
    lines = [
        f"Заявка №{lead.pk}",
        f"Имя: {lead.name}",
        f"Телефон: {lead.phone}",
        f"Дата: {lead.created_at}",
    ]
    if getattr(lead, "ym_client_id", None):
        lines.append(f"ClientID Метрики: {lead.ym_client_id}")
    lines.extend(["", "Сообщение:", lead.message or "—"])
    body = "\n".join(lines)

    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None) or "noreply@artemadera.su"

    backend = getattr(settings, "EMAIL_BACKEND", "") or ""
    host = (getattr(settings, "EMAIL_HOST", None) or "").strip()
    connection = None
    if "smtp" in backend.lower() and not host:
        logger.warning(
            "EMAIL_BACKEND=smtp, но EMAIL_HOST пуст — отправка через console backend "
            "(смотрите stdout / логи процесса gunicorn)."
        )
        connection = get_connection(
            "django.core.mail.backends.console.EmailBackend",
            fail_silently=False,
        )

    try:
        send_mail(
            subject,
            body,
            from_email,
            recipients,
            fail_silently=False,
            connection=connection,
        )
        logger.info(
            "Письмо о заявке #%s отправлено получателям: %s (backend=%s)",
            lead.pk,
            ", ".join(recipients),
            backend if connection is None else "console (fallback)",
        )
    except Exception:
        logger.exception(
            "Ошибка отправки письма о заявке #%s. Проверьте SMTP в .env: "
            "EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_TLS; "
            "или для проверки: EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend",
            lead.pk,
        )
