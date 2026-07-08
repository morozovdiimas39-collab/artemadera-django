import logging
from xml.sax.saxutils import escape

from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.exceptions import TemplateDoesNotExist
from django.utils import timezone

from .models import ContactLead, BlogPost, BlogSection

logger = logging.getLogger(__name__)


def _is_xhr_contact(request):
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"


def _contact_post_message(request):
    """Текст заявки: квиз, калькулятор и обычные поля."""
    from_block = (request.POST.get("from_block") or "").strip()
    if from_block == "quiz":
        page = (request.POST.get("quiz_page") or "").strip()
        svc = (request.POST.get("quiz_service_label") or request.POST.get("quiz_service") or "").strip()
        house = (request.POST.get("quiz_house_label") or request.POST.get("quiz_house_type") or "").strip()
        area = (request.POST.get("quiz_area") or "").strip()
        area_unit = (request.POST.get("quiz_area_unit") or "м²").strip()
        parts = []
        if page:
            parts.append(f"страница: {page}")
        if svc:
            parts.append(f"задача: {svc}")
        if house:
            parts.append(f"объект/деталь: {house}")
        if area:
            parts.append(f"объём: {area} {area_unit}")
        return "Квиз. " + ("; ".join(parts) if parts else "")
    calc_slug = (request.POST.get("calculator_profile") or "").strip()
    if from_block == "calculator" and calc_slug:
        base = (request.POST.get("message") or "").strip()
        extra = f"Калькулятор: {calc_slug}"
        return f"{base}\n{extra}".strip() if base else extra
    return (request.POST.get("message") or "").strip()


_LEAD_TRAFFIC_FIELDS = (
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_content",
    "utm_term",
    "yclid",
    "gclid",
    "fbclid",
    "ymclid",
    "ym_client_id",
    "page_url",
    "landing_page",
    "referrer",
)


def _clean_lead_value(value, max_len=500):
    return (value or "").strip()[:max_len]


def _lead_traffic_kwargs(request):
    """UTM и источники перехода: берём из формы, с fallback на текущий запрос."""
    data = {}
    for field in _LEAD_TRAFFIC_FIELDS:
        limit = 32 if field == "ym_client_id" else 500 if field in ("page_url", "landing_page", "referrer") else 255
        data[field] = _clean_lead_value(request.POST.get(field) or request.GET.get(field), limit)

    if not data["page_url"]:
        data["page_url"] = request.build_absolute_uri(request.get_full_path())[:500]
    if not data["landing_page"]:
        data["landing_page"] = data["page_url"]
    if not data["referrer"]:
        data["referrer"] = _clean_lead_value(request.META.get("HTTP_REFERER"), 500)
    return data


def _lead_crm_deal_id(lead):
    """CRM/email обрабатываются signal'ом; ответ формы не должен падать из-за них."""
    try:
        deal = getattr(lead, "crm_deal", None)
    except Exception:
        logger.exception("Не удалось получить CRM-сделку для заявки #%s", lead.pk)
        return None
    return getattr(deal, "pk", None) or None


def _handle_contact_post(request, base_path):
    """Handle contact form POST. Returns redirect, JsonResponse, or None."""
    if request.method != "POST":
        return None
    if request.POST.get("form_type") != "contact":
        return None
    phone = (request.POST.get("phone") or "").strip()
    if not phone:
        if _is_xhr_contact(request):
            return JsonResponse({"ok": False, "error": "phone_required"}, status=400)
        return None
    try:
        lead = ContactLead.objects.create(
            name=(request.POST.get("name") or "").strip() or "—",
            phone=phone,
            message=_contact_post_message(request),
            **_lead_traffic_kwargs(request),
        )
        crm_deal_id = _lead_crm_deal_id(lead)
        if _is_xhr_contact(request):
            return JsonResponse(
                {"ok": True, "lead_id": lead.pk, "crm_deal_id": crm_deal_id}
            )
        from_block = (request.POST.get("from_block") or "").strip()
        if from_block == "measure":
            return redirect(f"{base_path}?sent=1&from=measure#zamer")
        if from_block == "quiz" or from_block == "calculator":
            return redirect(f"{base_path}?sent=1#quiz")
        if from_block == "callback_modal":
            return redirect(f"{base_path}?sent=1")
        return redirect(f"{base_path}?sent=1#contact")
    except Exception:
        logger.exception("Не удалось сохранить заявку с сайта")
        if _is_xhr_contact(request):
            return JsonResponse({"ok": False, "error": "server"}, status=503)
        return None


def lead_direct_status(request, token):
    """Кнопка из email: отметить заявку для CSV Яндекс.Директа."""
    try:
        value = TimestampSigner(salt="lead-direct-status").unsign(token)
        lead_id, status = value.split(":", 1)
    except (BadSignature, SignatureExpired, ValueError):
        return HttpResponse("Ссылка недействительна.", status=400)

    valid_statuses = {value for value, _ in ContactLead.DIRECT_STATUS_CHOICES}
    if status not in valid_statuses:
        return HttpResponse("Неизвестный статус.", status=400)

    try:
        lead = ContactLead.objects.get(pk=lead_id)
    except (ContactLead.DoesNotExist, ValueError):
        return HttpResponse("Заявка не найдена.", status=404)

    lead.direct_status = status
    lead.direct_status_updated_at = timezone.now()
    lead.save(update_fields=["direct_status", "direct_status_updated_at"])

    label = dict(ContactLead.DIRECT_STATUS_CHOICES).get(status, status)
    goal_by_status = {
        ContactLead.DIRECT_STATUS_IN_PROGRESS: "DIRECT_TARGET",
        ContactLead.DIRECT_STATUS_PAID: "DIRECT_PAID",
        ContactLead.DIRECT_STATUS_CANCELLED: "DIRECT_CANCELLED",
        ContactLead.DIRECT_STATUS_SPAM: "DIRECT_SPAM",
    }
    goal = goal_by_status.get(status, "DIRECT_STATUS_CHANGED")
    return HttpResponse(
        f"""
        <!doctype html>
        <html lang="ru">
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <title>Статус заявки обновлён</title>
          <!-- Yandex.Metrika counter -->
          <script type="text/javascript">
            (function(m,e,t,r,i,k,a){{
              m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};
              m[i].l=1*new Date();
              for (var j = 0; j < document.scripts.length; j++) {{if (document.scripts[j].src === r) {{ return; }}}}
              k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
            }})(window, document,'script','https://mc.yandex.ru/metrika/tag.js', 'ym');

            ym(87164937, 'init', {{webvisor:true, clickmap:true, referrer: document.referrer, url: location.href, accurateTrackBounce:true, trackLinks:true}});
            ym(87164937, 'reachGoal', 'DIRECT_STATUS_CHANGED', {{status: '{status}', lead_id: '{lead.pk}'}});
            ym(87164937, 'reachGoal', '{goal}', {{status: '{status}', lead_id: '{lead.pk}'}});
          </script>
          <noscript><div><img src="https://mc.yandex.ru/watch/87164937" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
          <!-- /Yandex.Metrika counter -->
        </head>
        <body style="margin:0;font-family:Arial,sans-serif;background:#1c120c;color:#fff;display:grid;min-height:100vh;place-items:center">
          <main style="max-width:560px;padding:32px;border:1px solid rgba(245,158,11,.35);border-radius:16px;background:rgba(255,255,255,.05)">
            <h1 style="margin:0 0 12px">Готово</h1>
            <p style="font-size:18px;line-height:1.5;margin:0">Заявка №{lead.pk} отмечена как: <strong>{label}</strong>.</p>
            <p style="color:#d6d3d1;line-height:1.5">CSV для Яндекс.Директа теперь отдаст этот статус при следующем скачивании по ссылке.</p>
          </main>
        </body>
        </html>
        """
    )


def index(request):
    redir = _handle_contact_post(request, "/")
    if redir:
        return redir
    contact_form_sent = request.GET.get("sent") == "1"
    return render(
        request,
        "home.html",
        {"contact_form_sent": contact_form_sent},
    )


def shlifovka(request):
    redir = _handle_contact_post(request, "/shlifovka")
    if redir:
        return redir
    contact_form_sent = False
    measure_form_sent = False
    if request.GET.get("sent") == "1":
        if request.GET.get("from") == "measure":
            measure_form_sent = True
        else:
            contact_form_sent = True
    return render(
        request,
        "shlifovka.html",
        {
            "contact_form_sent": contact_form_sent,
            "measure_form_sent": measure_form_sent,
        },
    )


def pokraska(request):
    redir = _handle_contact_post(request, "/pokraska")
    if redir:
        return redir
    contact_form_sent = request.GET.get("sent") == "1"
    return render(request, "pokraska.html", {"contact_form_sent": contact_form_sent})


def teplyy_shov(request):
    redir = _handle_contact_post(request, "/teplyy-shov")
    if redir:
        return redir
    contact_form_sent = request.GET.get("sent") == "1"
    return render(request, "teplyy-shov.html", {"contact_form_sent": contact_form_sent})


def generic_service(request, path):
    normalized_path = (path or "").strip("/")
    redir = _handle_contact_post(request, f"/{normalized_path}")
    if redir:
        return redir
    contact_form_sent = request.GET.get("sent") == "1"
    template_name = normalized_path.replace("/", "_") + ".html"
    try:
        return render(request, template_name, {"contact_form_sent": contact_form_sent})
    except TemplateDoesNotExist:
        raise Http404


def blog_list(request):
    from .context_processors import _blog_defaults
    try:
        section = BlogSection.load()
        posts = list(
            BlogPost.objects.filter(is_active=True).order_by("sort_order", "-published_at", "pk")
        )
    except OperationalError:
        defaults = _blog_defaults()
        return render(request, "blog_list.html", defaults)
    if not posts:
        defaults = _blog_defaults()
        posts = defaults["blog_posts"]
    return render(request, "blog_list.html", {"blog_section": section, "blog_posts": posts})


def blog_detail(request, slug):
    try:
        post = get_object_or_404(BlogPost, slug=slug, is_active=True)
    except OperationalError:
        raise Http404
    try:
        section = BlogSection.load()
    except OperationalError:
        section = None
    return render(request, "blog_detail.html", {"post": post, "blog_section": section})


def robots_txt(request):
    host = request.get_host()
    scheme = "https" if not request.is_secure() and host == "artemadera.ru" else request.scheme
    content = "\n".join(
        [
            "User-agent: *",
            "Allow: /",
            "Disallow: /admin/",
            "Disallow: /export/",
            "Disallow: /lead-status/",
            f"Sitemap: {scheme}://{host}/sitemap.xml",
            "",
        ]
    )
    return HttpResponse(content, content_type="text/plain; charset=utf-8")


def sitemap_xml(request):
    from .models import BlogPost, SitePage

    host = request.get_host()
    scheme = "https" if not request.is_secure() and host == "artemadera.ru" else request.scheme
    base_url = f"{scheme}://{host}"
    paths = {"/", "/shlifovka", "/pokraska", "/teplyy-shov", "/blog"}

    for page_key in SitePage.objects.filter(is_active=True).values_list("page_key", flat=True):
        key = (page_key or "").strip("/")
        if key and key != "home":
            paths.add(f"/{key}")
    for slug in BlogPost.objects.filter(is_active=True).exclude(slug="").values_list("slug", flat=True):
        paths.add(f"/blog/{slug}/")

    urls = "".join(
        f"<url><loc>{escape(base_url + path)}</loc></url>"
        for path in sorted(paths)
    )
    xml = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>'
    return HttpResponse(xml, content_type="application/xml; charset=utf-8")
