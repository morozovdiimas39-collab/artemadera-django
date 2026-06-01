from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0037_leademailsettings_smtp_host_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="contactlead",
            name="page_url",
            field=models.URLField(blank=True, max_length=500, verbose_name="Страница заявки"),
        ),
        migrations.AddField(
            model_name="contactlead",
            name="landing_page",
            field=models.URLField(blank=True, max_length=500, verbose_name="Посадочная страница"),
        ),
        migrations.AddField(
            model_name="contactlead",
            name="referrer",
            field=models.URLField(blank=True, max_length=500, verbose_name="Referrer"),
        ),
        migrations.AddField(
            model_name="contactlead",
            name="utm_source",
            field=models.CharField(blank=True, max_length=255, verbose_name="UTM source"),
        ),
        migrations.AddField(
            model_name="contactlead",
            name="utm_medium",
            field=models.CharField(blank=True, max_length=255, verbose_name="UTM medium"),
        ),
        migrations.AddField(
            model_name="contactlead",
            name="utm_campaign",
            field=models.CharField(blank=True, max_length=255, verbose_name="UTM campaign"),
        ),
        migrations.AddField(
            model_name="contactlead",
            name="utm_content",
            field=models.CharField(blank=True, max_length=255, verbose_name="UTM content"),
        ),
        migrations.AddField(
            model_name="contactlead",
            name="utm_term",
            field=models.CharField(blank=True, max_length=255, verbose_name="UTM term"),
        ),
        migrations.AddField(
            model_name="contactlead",
            name="yclid",
            field=models.CharField(blank=True, max_length=255, verbose_name="Yandex Click ID"),
        ),
        migrations.AddField(
            model_name="contactlead",
            name="gclid",
            field=models.CharField(blank=True, max_length=255, verbose_name="Google Click ID"),
        ),
        migrations.AddField(
            model_name="contactlead",
            name="fbclid",
            field=models.CharField(blank=True, max_length=255, verbose_name="Facebook Click ID"),
        ),
        migrations.AddField(
            model_name="contactlead",
            name="ymclid",
            field=models.CharField(blank=True, max_length=255, verbose_name="Yandex Metrika Click ID"),
        ),
    ]
