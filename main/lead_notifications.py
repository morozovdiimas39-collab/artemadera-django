"""Письма при новых заявках с сайта (ContactLead)."""
from __future__ import annotations

import logging
import re
from smtplib import SMTPDataError

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
        or "https://artemadera.ru"
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
    env_login = (getattr(settings, "EMAIL_HOST_USER", "") or "").strip()
    env_password = (getattr(settings, "EMAIL_HOST_PASSWORD", "") or "").strip()
    cfg_login = (getattr(cfg, "smtp_login", "") or "").strip()
    cfg_password = (getattr(cfg, "smtp_password", "") or "").strip()
    login = cfg_login or env_login
    password = cfg_password or env_password
    from_email = (
        (getattr(cfg, "from_email", "") or "").strip()
        or login
        or getattr(settings, "DEFAULT_FROM_EMAIL", None)
        or "noreply@artemadera.ru"
    )
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
                timeout=10,
                fail_silently=False,
            ),
            from_email,
            f"smtp://{login}@{host}:{port}",
        )

    backend = getattr(settings, "EMAIL_BACKEND", "") or ""
    if "smtp" in backend.lower() and not (getattr(settings, "EMAIL_HOST", "") or "").strip():
        return (
            get_connection("django.core.mail.backends.console.EmailBackend", fail_silently=False),
            from_email,
            "console fallback: EMAIL_HOST пуст",
        )

    return (
        None,
        from_email,
        backend or "default",
    )


def _yandex_ssl_fallback_connection(cfg):
    env_login = (getattr(settings, "EMAIL_HOST_USER", "") or "").strip()
    env_password = (getattr(settings, "EMAIL_HOST_PASSWORD", "") or "").strip()
    login = (getattr(cfg, "smtp_login", "") or "").strip() or env_login
    password = (getattr(cfg, "smtp_password", "") or "").strip() or env_password
    from_email = (
        (getattr(cfg, "from_email", "") or "").strip()
        or login
        or getattr(settings, "DEFAULT_FROM_EMAIL", None)
        or "noreply@artemadera.ru"
    )
    host = _smtp_host_for_login(login, (getattr(cfg, "smtp_host", "") or "").strip())
    if not login or not password or host != "smtp.yandex.ru":
        return None, from_email, ""
    return (
        get_connection(
            "django.core.mail.backends.smtp.EmailBackend",
            host=host,
            port=465,
            username=login,
            password=password,
            use_tls=False,
            use_ssl=True,
            timeout=10,
            fail_silently=False,
        ),
        from_email,
        f"smtps://{login}@{host}:465",
    )


def _send_email_message(subject, body, html_body, from_email, recipients, connection):
    message = EmailMultiAlternatives(
        subject,
        body,
        from_email,
        recipients,
        connection=connection,
    )
    if html_body:
        message.attach_alternative(html_body, "text/html")
    return message.send(fail_silently=False)


def _is_spam_reject(error) -> bool:
    if not isinstance(error, SMTPDataError):
        return False
    message = error.smtp_error.decode(errors="ignore") if isinstance(error.smtp_error, bytes) else str(error.smtp_error)
    return error.smtp_code == 554 and "spam" in message.lower()


def _build_safe_plain_body(lead) -> str:
    lines = [
        f"Новая заявка с сайта #{lead.pk}",
        f"Имя: {lead.name}",
        f"Телефон: {lead.phone}",
        f"Дата: {lead.created_at}",
        "",
        "Сообщение:",
        lead.message or "—",
    ]
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
        lines.extend(["", "Источник заявки:", *traffic_lines])
    lines.extend(
        [
            "",
            "Статус для CSV можно изменить в CRM в карточке заявки.",
        ]
    )
    return "\n".join(lines)


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

    raw = "\n".join(
        part
        for part in (
            (cfg.notification_emails or "").strip(),
            (getattr(settings, "LEAD_NOTIFICATION_EMAILS", "") or "").strip(),
        )
        if part
    ) or (getattr(settings, "EMAIL_HOST_USER", "") or "").strip()
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
        _send_email_message(subject, body, html_body, from_email, recipients, connection)
        logger.info(
            "Письмо о заявке #%s отправлено получателям: %s (backend=%s)",
            lead.pk,
            ", ".join(recipients),
            backend_label,
        )
    except Exception as primary_error:
        if _is_spam_reject(primary_error):
            logger.warning(
                "Основное HTML-письмо о заявке #%s отклонено SMTP как спам. "
                "Пробуем отправить простой текстовый вариант.",
                lead.pk,
            )
            for retry_label, retry_body in (
                ("plain-status-links", body),
                ("plain-safe", _build_safe_plain_body(lead)),
            ):
                try:
                    retry_connection, retry_from_email, retry_backend_label = _email_connection_from_config(cfg)
                    _send_email_message(
                        subject,
                        retry_body,
                        "",
                        retry_from_email,
                        recipients,
                        retry_connection,
                    )
                    logger.info(
                        "Письмо о заявке #%s отправлено простым текстом (%s, backend=%s)",
                        lead.pk,
                        retry_label,
                        retry_backend_label,
                    )
                    return
                except Exception as retry_error:
                    logger.warning(
                        "Текстовая отправка письма о заявке #%s не прошла (%s): %s",
                        lead.pk,
                        retry_label,
                        retry_error,
                    )

        fallback, fallback_from, fallback_label = _yandex_ssl_fallback_connection(cfg)
        if fallback and backend_label != fallback_label:
            try:
                _send_email_message(
                    subject, body, html_body, fallback_from, recipients, fallback
                )
                logger.info(
                    "Письмо о заявке #%s отправлено через резервный SMTP: %s",
                    lead.pk,
                    fallback_label,
                )
                return
            except Exception:
                logger.exception(
                    "Ошибка отправки письма о заявке #%s через основной и резервный SMTP. "
                    "Основная ошибка: %s",
                    lead.pk,
                    primary_error,
                )
                return
        logger.exception("Ошибка отправки письма о заявке #%s", lead.pk)


def send_lead_test_email() -> int:
    """Отправляет тестовое письмо из админки. Исключения отдаём наверх, чтобы показать ошибку."""
    from .models import LeadEmailSettings

    cfg = LeadEmailSettings.load()
    recipients = parse_notification_emails((cfg.notification_emails or "").strip())
    if not recipients:
        raise ValueError("В поле «Email для уведомлений» нет валидного адреса получателя.")

    subject = "ArteMadera: тест отправки заявок"
    body = "Это тестовое письмо из админки ArteMadera. Если оно дошло, заявки тоже будут уходить."
    html_body = "<p>Это тестовое письмо из админки ArteMadera.</p><p>Если оно дошло, заявки тоже будут уходить.</p>"
    connection, from_email, backend_label = _email_connection_from_config(cfg)
    try:
        return _send_email_message(
            subject, body, html_body, from_email, recipients, connection
        )
    except Exception:
        fallback, fallback_from, fallback_label = _yandex_ssl_fallback_connection(cfg)
        if not fallback or backend_label == fallback_label:
            raise
        return _send_email_message(
            subject, body, html_body, fallback_from, recipients, fallback
        )
