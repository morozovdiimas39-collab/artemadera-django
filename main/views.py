from django.shortcuts import render, redirect
from django.template.exceptions import TemplateDoesNotExist
from django.db.utils import OperationalError

from .models import ContactLead

try:
    from crm.services import create_deal_from_site_lead
except ImportError:
    create_deal_from_site_lead = None


def _handle_contact_post(request, base_path):
    """Handle contact form POST. Returns redirect response or None."""
    if request.method != "POST":
        return None
    if request.POST.get("form_type") != "contact":
        return None
    phone = (request.POST.get("phone") or "").strip()
    if not phone:
        return None
    try:
        lead = ContactLead.objects.create(
            name=(request.POST.get("name") or "").strip() or "—",
            phone=phone,
            message=(request.POST.get("message") or "").strip(),
        )
        if create_deal_from_site_lead:
            try:
                create_deal_from_site_lead(
                    lead,
                    from_block=request.POST.get("from_block") or None,
                )
            except Exception:
                pass
        anchor = "quiz" if request.POST.get("from_block") == "calculator" else "contact"
        return redirect(f"{base_path}?sent=1#{anchor}")
    except OperationalError:
        return None


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
    measure_form_sent = False
    if request.method == "POST" and request.POST.get("form_type") == "contact":
        phone = (request.POST.get("phone") or "").strip()
        if phone:
            try:
                lead = ContactLead.objects.create(
                    name=(request.POST.get("name") or "").strip() or "—",
                    phone=phone,
                    message=(request.POST.get("message") or "").strip(),
                )
                if create_deal_from_site_lead:
                    try:
                        create_deal_from_site_lead(
                            lead,
                            from_block=request.POST.get("from_block") or None,
                        )
                    except Exception:
                        pass
                if request.POST.get("from_block") == "measure":
                    return redirect("/shlifovka?sent=1&from=measure#zamer")
                return redirect("/shlifovka?sent=1#contact")
            except OperationalError:
                pass
    contact_form_sent = False
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
