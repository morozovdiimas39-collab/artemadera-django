from django.db import migrations


ROWS = [
    {
        "title": "Обсада оконного проёма",
        "before_image": "before_after/obsada-window-before.webp",
        "after_image": "before_after/obsada-window-after.webp",
        "sort_order": 0,
    },
    {
        "title": "Обсада дверного проёма",
        "before_image": "before_after/obsada-door-before.webp",
        "after_image": "before_after/obsada-door-after.webp",
        "sort_order": 1,
    },
]


def apply_obsada_before_after(apps, schema_editor):
    SitePage = apps.get_model("main", "SitePage")
    BeforeAfterItem = apps.get_model("main", "BeforeAfterItem")

    page = SitePage.objects.filter(page_key="obsada").first()
    if not page:
        return

    BeforeAfterItem.objects.filter(page=page).delete()
    for row in ROWS:
        BeforeAfterItem.objects.create(
            page=page,
            title=row["title"],
            before_image=row["before_image"],
            after_image=row["after_image"],
            before_static="",
            after_static="",
            sort_order=row["sort_order"],
            is_active=True,
        )


def revert_obsada_before_after(apps, schema_editor):
    SitePage = apps.get_model("main", "SitePage")
    BeforeAfterItem = apps.get_model("main", "BeforeAfterItem")

    page = SitePage.objects.filter(page_key="obsada").first()
    if page:
        BeforeAfterItem.objects.filter(page=page).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0062_clean_obsada_service_tiles"),
    ]

    operations = [
        migrations.RunPython(apply_obsada_before_after, revert_obsada_before_after),
    ]
