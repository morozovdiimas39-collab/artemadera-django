from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0026_work_process_four_chronological_stages"),
    ]

    operations = [
        migrations.AddField(
            model_name="contactlead",
            name="ym_client_id",
            field=models.CharField(
                blank=True,
                help_text="Числовой идентификатор для офлайн-конверсий в Директе; можно передавать из формы скрытым полем.",
                max_length=32,
                verbose_name="ClientID Метрики (_ym_uid)",
            ),
        ),
    ]
