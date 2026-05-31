import json
from types import SimpleNamespace

from django.db.utils import OperationalError

from .models import CalculatorProfile, CalculatorOption, CalculatorMaterial, CalculatorConfig

PATH_CALCULATOR_SLUG = {
    "/": "home",
    "/shlifovka": "shlifovka",
    "/pokraska": "pokraska",
    "/teplyy-shov": "teplyy-shov",
    "/obsada": "obsada",
    "/obsada/okna": "obsada",
    "/obsada/dveri": "obsada",
    "/kryshi": "kryshi",
    "/injeneriya": "injeneriya",
    "/otdelka/sten": "pokraska",
    "/otdelka/pola": "pokraska",
    "/otdelka/konopatka": "teplyy-shov",
    "/otdelka/shlifovka/brusa": "shlifovka",
    "/otdelka/shlifovka/sruba": "shlifovka",
    "/otdelka/shlifovka/lafeta": "shlifovka",
    "/otdelka/shlifovka/ocilindrovannogo-brevna": "shlifovka",
    "/otdelka/shlifovka/konsyerzhnaya": "shlifovka",
    "/otdelka/shlifovka/bani-i-sauny": "shlifovka",
    "/otdelochnye-raboty": "pokraska",
    "/proizvodstvo": "obsada",
    "/proizvodstvo/besedki": "obsada",
    "/proizvodstvo/falshbalki": "obsada",
    "/proizvodstvo/plintusy": "obsada",
}


def _format_rub(amount):
    return f"{int(amount):,}".replace(",", "\u00a0") + " \u20bd"


def resolve_calculator_slug(request):
    override = getattr(request, "calculator_profile_slug", None)
    if override:
        return override
    path = request.path.rstrip("/") or "/"
    return PATH_CALCULATOR_SLUG.get(path, "shlifovka")


def _legacy_materials_context():
    materials = [
        SimpleNamespace(key="srub", label="Сруб (бревенчатый)", price_per_unit=1200),
        SimpleNamespace(key="brus", label="Дом из бруса", price_per_unit=1100),
        SimpleNamespace(key="kleen", label="Клееный брус", price_per_unit=1000),
        SimpleNamespace(key="banya", label="Баня/сауна", price_per_unit=1500),
    ]
    config = SimpleNamespace(
        area_min=20,
        area_max=300,
        area_step=5,
        area_default=75,
        unit_type="sqm",
        unit_label="м²",
        options_label="Материал дома",
    )
    profile = SimpleNamespace(
        slug="shlifovka",
        badge_text="КАЛЬКУЛЯТОР",
        title="Онлайн-калькулятор",
        description="Узнайте примерную стоимость шлифовки.",
        perk_1="Бесплатный расчёт",
        perk_2="Перезвон за 30 минут",
        perk_3="Консультация специалиста",
        options_label="Материал дома",
        unit_type="sqm",
        unit_label="м²",
        show_service_picker=False,
        submit_button_text="Зафиксировать цену",
    )
    return profile, config, materials


def _profile_to_config(profile):
    return SimpleNamespace(
        area_min=profile.area_min,
        area_max=profile.area_max,
        area_step=profile.area_step,
        area_default=profile.area_default,
        unit_type=profile.unit_type,
        unit_label=profile.unit_label,
        options_label=profile.options_label,
    )


def _build_profile_payload(profile, options):
    prices = {o.key: o.price_per_unit for o in options}
    default_key = options[0].key if options else ""
    default_price = prices.get(default_key, 0)
    if profile.unit_type == CalculatorProfile.UNIT_FIXED:
        initial_total = default_price
    else:
        initial_total = profile.area_default * default_price
    return {
        "slug": profile.slug,
        "badge_text": profile.badge_text,
        "title": profile.title,
        "description": profile.description,
        "perk_1": profile.perk_1,
        "perk_2": profile.perk_2,
        "perk_3": profile.perk_3,
        "options_label": profile.options_label,
        "unit_type": profile.unit_type,
        "unit_label": profile.unit_label,
        "show_service_picker": profile.show_service_picker,
        "submit_button_text": profile.submit_button_text,
        "area_min": profile.area_min,
        "area_max": profile.area_max,
        "area_step": profile.area_step,
        "area_default": profile.area_default,
        "options": [
            {
                "key": o.key,
                "label": o.label,
                "price": o.price_per_unit,
            }
            for o in options
        ],
        "default_option": default_key,
        "initial_total": initial_total,
    }


def build_calculator_context(request, slug=None):
    slug = slug or resolve_calculator_slug(request)

    try:
        profile = CalculatorProfile.objects.filter(slug=slug, is_active=True).first()
        if not profile:
            profile = CalculatorProfile.objects.filter(slug="shlifovka", is_active=True).first()
        if not profile:
            return _legacy_context()

        options = list(
            profile.options.filter(is_active=True).order_by("sort_order", "pk")
        )
        if not options:
            return _legacy_context()

        config = _profile_to_config(profile)
        prices = {o.key: o.price_per_unit for o in options}
        default_key = options[0].key
        default_price = prices.get(default_key, 0)
        if profile.unit_type == CalculatorProfile.UNIT_FIXED:
            initial_total = default_price
        else:
            initial_total = profile.area_default * default_price

        service_choices = []
        if profile.show_service_picker:
            service_choices = list(
                profile.service_choices.filter(is_active=True)
                .select_related("target_profile")
                .order_by("sort_order", "pk")
            )

        profiles_json = {}
        if profile.show_service_picker:
            all_profiles = (
                CalculatorProfile.objects.filter(is_active=True)
                .prefetch_related("options")
                .order_by("sort_order", "pk")
            )
            for p in all_profiles:
                if p.show_service_picker:
                    continue
                p_options = [o for o in p.options.all() if o.is_active]
                if not p_options:
                    continue
                profiles_json[p.slug] = _build_profile_payload(p, p_options)

        return {
            "calculator_profile": profile,
            "calculator_config": config,
            "calculator_options": options,
            "calculator_materials": options,
            "calculator_prices_json": json.dumps(prices),
            "calculator_default_material": default_key,
            "calculator_default_option": default_key,
            "calculator_initial_total": _format_rub(initial_total),
            "calculator_service_choices": service_choices,
            "calculator_profiles_json": json.dumps(profiles_json, ensure_ascii=False),
            "calculator_show_standalone": False,
        }
    except OperationalError:
        return _legacy_context()


def _legacy_context():
    profile, config, materials = _legacy_materials_context()
    prices = {m.key: m.price_per_unit for m in materials}
    default_key = materials[0].key
    initial_total = config.area_default * prices[default_key]
    return {
        "calculator_profile": profile,
        "calculator_config": config,
        "calculator_options": materials,
        "calculator_materials": materials,
        "calculator_prices_json": json.dumps(prices),
        "calculator_default_material": default_key,
        "calculator_default_option": default_key,
        "calculator_initial_total": _format_rub(initial_total),
        "calculator_service_choices": [],
        "calculator_profiles_json": "{}",
        "calculator_show_standalone": False,
    }
