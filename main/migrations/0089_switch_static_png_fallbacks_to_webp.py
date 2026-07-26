from django.db import migrations


REPLACEMENTS = {
    "images/team.png": "images/team.webp",
    "images/quiz/quiz_shlifovka_1776809850085.png": "images/quiz/quiz_shlifovka_1776809850085.webp",
    "images/quiz/quiz_pokraska_1776809864700.png": "images/quiz/quiz_pokraska_1776809864700.webp",
    "images/quiz/quiz_konopatka_1776809894304.png": "images/quiz/quiz_konopatka_1776809894304.webp",
    "images/quiz/quiz_brus_1776809793588.png": "images/quiz/quiz_brus_1776809793588.webp",
    "images/quiz/quiz_srub_1776809774832.png": "images/quiz/quiz_srub_1776809774832.webp",
    "images/quiz/quiz_banja_1776809825595.png": "images/quiz/quiz_banja_1776809825595.webp",
    "images/quiz/quiz_banja_modern_1776810582042.png": "images/quiz/quiz_banja_modern_1776810582042.webp",
    "images/quiz/quiz_kleyeny_1776809809396.png": "images/quiz/quiz_kleyeny_1776809809396.webp",
    "images/quiz/quiz_antiseptik_1776809879943.png": "images/quiz/quiz_antiseptik_1776809879943.webp",
    "images/quiz/quiz_calendar_1776809931720.png": "images/quiz/quiz_calendar_1776809931720.webp",
    "images/quiz/quiz_area_1776809914472.png": "images/quiz/quiz_area_1776809914472.webp",
    "images/whyus_tools_1776809484018.png": "images/whyus_tools_1776809484018.webp",
    "images/whyus_eco_1776809551533.png": "images/whyus_eco_1776809551533.webp",
    "images/whyus_price_1776809529581.png": "images/whyus_price_1776809529581.webp",
    "images/whyus_time_1776809500549.png": "images/whyus_time_1776809500549.webp",
    "images/whyus_team_1776809465370.png": "images/whyus_team_1776809465370.webp",
    "images/whyus_quality_1776809515137.png": "images/whyus_quality_1776809515137.webp",
    "images/contact_bg.png": "images/contact_bg.webp",
}

TARGETS = (
    ("main", "Service", "static_image"),
    ("main", "SitePage", "hero_static_image"),
    ("main", "PortfolioProject", "static_image"),
    ("main", "PortfolioProjectImage", "static_image"),
    ("main", "ExperienceSection", "static_image"),
    ("main", "BlogPost", "static_image"),
)


def replace_values(apps, replacements):
    for app_label, model_name, field_name in TARGETS:
        Model = apps.get_model(app_label, model_name)
        for old, new in replacements.items():
            Model.objects.filter(**{field_name: old}).update(**{field_name: new})


def forwards(apps, schema_editor):
    replace_values(apps, REPLACEMENTS)


def backwards(apps, schema_editor):
    replace_values(apps, {new: old for old, new in REPLACEMENTS.items()})


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0088_seo_primary_h1_alignment"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
