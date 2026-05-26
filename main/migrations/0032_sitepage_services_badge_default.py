from django.db import migrations, models


def clear_generic_services_badge(apps, schema_editor):
    """
    Раньше у services_badge в модели был default «Наши услуги», и он попадал в БД
    для всех страниц без явных полей заголовка — блок выглядел как с главной/шлифовки.
    """
    SitePage = apps.get_model("main", "SitePage")
    SitePage.objects.filter(
        services_badge="Наши услуги",
        services_title_white="",
        services_title_accent="",
    ).update(services_badge="")


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0031_shlifovka_concierge_banya_pages"),
    ]

    operations = [
        migrations.RunPython(clear_generic_services_badge, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="sitepage",
            name="services_badge",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Пусто — в блоке на странице подставится короткая подпись из названия страницы.",
                max_length=64,
                verbose_name="Бейдж блока услуг",
            ),
        ),
    ]
