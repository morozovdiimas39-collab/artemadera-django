from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.exceptions import TemplateDoesNotExist
from django.db.utils import OperationalError
from django.utils import timezone

from .models import ContactLead, BlogPost, BlogSection

try:
    from crm.services import create_deal_from_site_lead
except ImportError:
    create_deal_from_site_lead = None


def _is_xhr_contact(request):
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"


def _contact_post_message(request):
    """Текст заявки: квиз, калькулятор и обычные поля."""
    from_block = (request.POST.get("from_block") or "").strip()
    if from_block == "quiz":
        svc = (request.POST.get("quiz_service") or "").strip()
        house = (request.POST.get("quiz_house_type") or "").strip()
        area = (request.POST.get("quiz_area") or "").strip()
        parts = []
        if svc:
            parts.append(f"услуга: {svc}")
        if house:
            parts.append(f"тип дома: {house}")
        if area:
            parts.append(f"площадь: {area} м²")
        return "Квиз. " + ("; ".join(parts) if parts else "")
    calc_slug = (request.POST.get("calculator_profile") or "").strip()
    if from_block == "calculator" and calc_slug:
        base = (request.POST.get("message") or "").strip()
        extra = f"Калькулятор: {calc_slug}"
        return f"{base}\n{extra}".strip() if base else extra
    return (request.POST.get("message") or "").strip()


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
        )
        if create_deal_from_site_lead:
            try:
                create_deal_from_site_lead(
                    lead,
                    from_block=request.POST.get("from_block") or None,
                )
            except Exception:
                pass
        if _is_xhr_contact(request):
            return JsonResponse({"ok": True})
        from_block = (request.POST.get("from_block") or "").strip()
        if from_block == "measure":
            return redirect(f"{base_path}?sent=1&from=measure#zamer")
        if from_block == "quiz" or from_block == "calculator":
            return redirect(f"{base_path}?sent=1#quiz")
        if from_block == "callback_modal":
            return redirect(f"{base_path}?sent=1")
        return redirect(f"{base_path}?sent=1#contact")
    except OperationalError:
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
    return HttpResponse(
        f"""
        <!doctype html>
        <html lang="ru">
        <head><meta charset="utf-8"><title>Статус заявки обновлён</title></head>
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
    redir = _handle_contact_post(request, f"/{path}")
    if redir:
        return redir
    contact_form_sent = request.GET.get("sent") == "1"
    template_name = path.replace("/", "_") + ".html"
    try:
        return render(request, template_name, {"contact_form_sent": contact_form_sent})
    except TemplateDoesNotExist:
        return render(request, "home.html")


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
