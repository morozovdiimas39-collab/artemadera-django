"""Письма при новых заявках с сайта (ContactLead)."""
from __future__ import annotations

import logging
import re

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection
from django.core.signing import TimestampSigner
from django.urls import reverse
from django.utils.html import escape

logger = logging.getLogger(__name__)

LEAD_STATUS_LABELS = {
    "IN_PROGRESS": "Целевой",
    "PAID": "Оплачен",
    "CANCELLED": "Нецелевой",
    "SPAM": "Спам",
}


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


def signed_lead_status_token(lead_id: int, status: str) -> str:
    return TimestampSigner(salt="lead-direct-status").sign(f"{lead_id}:{status}")


def _site_base_url() -> str:
    raw = (
        getattr(settings, "SITE_BASE_URL", "")
        or getattr(settings, "DEFAULT_SITE_URL", "")
        or "https://artemadera.su"
    )
    return str(raw).strip().rstrip("/")


def lead_status_action_url(lead, status: str) -> str:
    token = signed_lead_status_token(lead.pk, status)
    return _site_base_url() + reverse("lead_direct_status", args=[token])


def _smtp_host_for_login(login: str, host: str) -> str:
    if host:
        return host
    if login:
        return "smtp.yandex.ru"
    return ""


def _email_connection_from_config(cfg):
    login = (getattr(cfg, "smtp_login", "") or "").strip() or (getattr(settings, "EMAIL_HOST_USER", "") or "").strip()
    password = (getattr(cfg, "smtp_password", "") or "").strip() or (getattr(settings, "EMAIL_HOST_PASSWORD", "") or "").strip()
    host = _smtp_host_for_login(login, (getattr(cfg, "smtp_host", "") or getattr(settings, "EMAIL_HOST", "") or "").strip())
    port = int(getattr(cfg, "smtp_port", None) or getattr(settings, "EMAIL_PORT", 587) or 587)
    use_ssl = bool(getattr(cfg, "smtp_use_ssl", False) or getattr(settings, "EMAIL_USE_SSL", False))
    use_tls = bool(getattr(cfg, "smtp_use_tls", True) if not use_ssl else False)

    if login and password and host:
        return (
            get_connection(
                "django.core.mail.backends.smtp.EmailBackend",
                host=host,
                port=port,
                username=login,
                password=password,
                use_tls=use_tls,
                use_ssl=use_ssl,
                fail_silently=False,
            ),
            login,
            f"smtp://{login}@{host}:{port}",
        )

    backend = getattr(settings, "EMAIL_BACKEND", "") or ""
    if "smtp" in backend.lower() and not (getattr(settings, "EMAIL_HOST", "") or "").strip():
        return (
            get_connection("django.core.mail.backends.console.EmailBackend", fail_silently=False),
            getattr(settings, "DEFAULT_FROM_EMAIL", None) or "noreply@artemadera.su",
            "console fallback: EMAIL_HOST пуст",
        )

    return (
        None,
        getattr(settings, "DEFAULT_FROM_EMAIL", None) or "noreply@artemadera.su",
        backend or "default",
    )


def _build_email_bodies(lead) -> tuple[str, str]:
    labels = LEAD_STATUS_LABELS
    action_lines = [
        f"{label}: {lead_status_action_url(lead, status)}"
        for status, label in labels.items()
    ]
    text_lines = [
        f"Заявка №{lead.pk}",
        f"Имя: {lead.name}",
        f"Телефон: {lead.phone}",
        f"Дата: {lead.created_at}",
        "",
        "Сообщение:",
        lead.message or "—",
        "",
        "Отметить для CSV Директа:",
        *action_lines,
    ]
    if getattr(lead, "ym_client_id", None):
        text_lines.insert(4, f"ClientID Метрики: {lead.ym_client_id}")
    traffic_lines = []
    for label, attr in (
        ("Страница заявки", "page_url"),
        ("Посадочная страница", "landing_page"),
        ("Referrer", "referrer"),
        ("utm_source", "utm_source"),
        ("utm_medium", "utm_medium"),
        ("utm_campaign", "utm_campaign"),
        ("utm_content", "utm_content"),
        ("utm_term", "utm_term"),
        ("yclid", "yclid"),
        ("gclid", "gclid"),
        ("fbclid", "fbclid"),
        ("ymclid", "ymclid"),
    ):
        value = getattr(lead, attr, "") or ""
        if value:
            traffic_lines.append(f"{label}: {value}")
    if traffic_lines:
        text_lines.extend(["", "Источник заявки:", *traffic_lines])

    rows = [
        ("Имя", lead.name),
        ("Телефон", lead.phone),
        ("Дата", lead.created_at),
    ]
    if getattr(lead, "ym_client_id", None):
        rows.append(("ClientID Метрики", lead.ym_client_id))
    for label, attr in (
        ("Страница заявки", "page_url"),
        ("Посадочная страница", "landing_page"),
        ("Referrer", "referrer"),
        ("utm_source", "utm_source"),
        ("utm_medium", "utm_medium"),
        ("utm_campaign", "utm_campaign"),
        ("utm_content", "utm_content"),
        ("utm_term", "utm_term"),
        ("yclid", "yclid"),
        ("gclid", "gclid"),
        ("fbclid", "fbclid"),
        ("ymclid", "ymclid"),
    ):
        value = getattr(lead, attr, "") or ""
        if value:
            rows.append((label, value))
    rows.append(("Сообщение", lead.message or "—"))

    detail_rows = "".join(
        f"<tr><td style=\"padding:8px 12px;color:#6b7280;border-bottom:1px solid #eee\">{escape(label)}</td>"
        f"<td style=\"padding:8px 12px;color:#111827;border-bottom:1px solid #eee\">{escape(value)}</td></tr>"
        for label, value in rows
    )
    buttons = "".join(
        f"<a href=\"{escape(lead_status_action_url(lead, status))}\" "
        "style=\"display:inline-block;margin:0 8px 10px 0;padding:12px 16px;border-radius:8px;"
        "background:#1f2937;color:#fff;text-decoration:none;font-weight:700\">"
        f"{escape(label)}</a>"
        for status, label in labels.items()
    )
    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:720px;color:#111827">
      <h2 style="margin:0 0 16px">Новая заявка с сайта #{lead.pk}</h2>
      <table style="width:100%;border-collapse:collapse;margin-bottom:20px">{detail_rows}</table>
      <h3 style="margin:0 0 12px">Статус для CSV Директа</h3>
      <p style="margin:0 0 12px;color:#4b5563">Нажмите кнопку, и статус заявки обновится в файле конверсий.</p>
      <div>{buttons}</div>
    </div>
    """
    return "\n".join(text_lines), html


def send_lead_created_email(lead) -> None:
    """Отправляет письмо о новой заявке, если в админке заданы адреса."""
    from .models import LeadEmailSettings

    try:
        cfg = LeadEmailSettings.load()
    except Exception:
        logger.exception("LeadEmailSettings.load failed — миграции применены? (main.0030)")
        return

    raw = (
        (cfg.notification_emails or "").strip()
        or (getattr(settings, "LEAD_NOTIFICATION_EMAILS", "") or "").strip()
        or (getattr(settings, "EMAIL_HOST_USER", "") or "").strip()
    )
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
    body, html_body = _build_email_bodies(lead)

    connection, from_email, backend_label = _email_connection_from_config(cfg)

    try:
        message = EmailMultiAlternatives(
            subject,
            body,
            from_email,
            recipients,
            connection=connection,
        )
        message.attach_alternative(html_body, "text/html")
        message.send(fail_silently=False)
        logger.info(
            "Письмо о заявке #%s отправлено получателям: %s (backend=%s)",
            lead.pk,
            ", ".join(recipients),
            backend_label,
        )
    except Exception:
        logger.exception(
            "Ошибка отправки письма о заявке #%s. Проверьте SMTP в .env: "
            "EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_TLS; "
            "или для проверки: EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend",
            lead.pk,
        )


def send_lead_test_email() -> int:
    """Отправляет тестовое письмо из админки. Исключения отдаём наверх, чтобы показать ошибку."""
    from .models import LeadEmailSettings

    cfg = LeadEmailSettings.load()
    recipients = parse_notification_emails((cfg.notification_emails or "").strip())
    if not recipients:
        raise ValueError("В поле «Email для уведомлений» нет валидного адреса получателя.")

    connection, from_email, _backend_label = _email_connection_from_config(cfg)
    message = EmailMultiAlternatives(
        "ArteMadera: тест отправки заявок",
        "Это тестовое письмо из админки ArteMadera. Если оно дошло, заявки тоже будут уходить.",
        from_email,
        recipients,
        connection=connection,
    )
    message.attach_alternative(
        "<p>Это тестовое письмо из админки ArteMadera.</p><p>Если оно дошло, заявки тоже будут уходить.</p>",
        "text/html",
    )
    return message.send(fail_silently=False)
