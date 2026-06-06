from django.db import migrations


def apply_document_updates(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    ExperienceAdvantage = apps.get_model("main", "ExperienceAdvantage")
    FaqItem = apps.get_model("main", "FaqItem")
    PortfolioProject = apps.get_model("main", "PortfolioProject")

    Service.objects.filter(slug="okosyachka").update(
        name="Обсада",
        short_description="Компенсация усадки и защита оконных и дверных проёмов.",
    )
    Service.objects.filter(slug="obsada-okna").update(
        name="Окна",
        short_description="Обсадные короба и подготовка оконных проёмов.",
    )

    ExperienceAdvantage.objects.filter(title="Собственное производство").update(
        description=(
            "Обсада, наличники, декоративные панели, плинтусы, фальшбалки "
            "и другие погонажные изделия."
        )
    )

    FaqItem.objects.filter(question="Можно ли шлифовать деревянный дом зимой?").update(
        answer=(
            "Да. На объекте создаём временный тепловой контур и используем "
            "специальное оборудование, чтобы поддерживать нужную температуру "
            "и влажность. Так шлифовка и подготовка под покраску возможны круглый год."
        )
    )
    FaqItem.objects.filter(question="Даёте ли гарантию на работы?").update(
        answer=(
            "Да, гарантия на выполненные работы прописывается в договоре. "
            "Срок зависит от вида работ и применяемых составов — обычно до 3 лет."
        )
    )
    FaqItem.objects.filter(question="Работаете ли в Москве и области?").update(
        question="В каких регионах вы выполняете работы?",
        answer="Выполняем работы во всех регионах РФ.",
    )

    holiday_base = PortfolioProject.objects.filter(title="База отдыха").first()
    if holiday_base:
        holiday_base.summary = "Каркасные дома для базы отдыха"
        holiday_base.description = (
            "Построили каркасные дома для базы отдыха под ключ: от основных "
            "строительных работ до подготовки и финишной отделки объектов."
        )
        holiday_base.work_types = "строительство под ключ, отделка"
        holiday_base.house_type = "other"
        holiday_base.save(
            update_fields=["summary", "description", "work_types", "house_type"]
        )

    for project in PortfolioProject.objects.filter(description="").order_by("pk"):
        summary = (project.summary or "").strip()
        work_types = (project.work_types or "").strip()
        location = (project.location or "").strip()
        parts = []
        if summary:
            parts.append(f"Объект: {summary}.")
        if work_types:
            parts.append(f"Выполненные работы: {work_types}.")
        if location:
            parts.append(f"Локация: {location}.")
        if parts:
            project.description = " ".join(parts)
            project.save(update_fields=["description"])


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0042_alter_reviewssection_yandex_rating"),
    ]

    operations = [
        migrations.RunPython(apply_document_updates, migrations.RunPython.noop),
    ]
