from django.db import migrations


def backfill_missing_crm_deals(apps, schema_editor):
    ContactLead = apps.get_model("main", "ContactLead")
    CrmContact = apps.get_model("crm", "CrmContact")
    CrmDeal = apps.get_model("crm", "CrmDeal")
    CrmLeadSource = apps.get_model("crm", "CrmLeadSource")
    CrmPipeline = apps.get_model("crm", "CrmPipeline")
    CrmStage = apps.get_model("crm", "CrmStage")

    pipeline = CrmPipeline.objects.filter(is_default=True, is_active=True).first()
    if not pipeline:
        pipeline = CrmPipeline.objects.create(
            name="Продажи",
            slug="sales",
            is_default=True,
            sort_order=0,
        )

    stage = (
        CrmStage.objects.filter(pipeline=pipeline, stage_type="open")
        .order_by("sort_order", "pk")
        .first()
    )
    if not stage:
        stage = CrmStage.objects.create(
            pipeline=pipeline,
            name="Новая заявка",
            stage_type="open",
            color="#78716c",
            sort_order=10,
        )

    source, _ = CrmLeadSource.objects.get_or_create(
        code="website_contact",
        defaults={"name": "Сайт — контакты", "sort_order": 0},
    )

    for lead in ContactLead.objects.filter(crm_deal__isnull=True).iterator():
        contact = CrmContact.objects.filter(phone=lead.phone).first()
        if not contact:
            contact = CrmContact.objects.create(
                name=lead.name if lead.name and lead.name != "—" else lead.phone,
                phone=lead.phone,
            )
        CrmDeal.objects.create(
            title=f"Заявка — {lead.phone}",
            contact=contact,
            pipeline=pipeline,
            stage=stage,
            source=source,
            description=lead.message or "",
            site_lead=lead,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("crm", "0001_initial"),
        ("main", "0044_use_company_email_sender"),
    ]

    operations = [
        migrations.RunPython(backfill_missing_crm_deals, migrations.RunPython.noop),
    ]
