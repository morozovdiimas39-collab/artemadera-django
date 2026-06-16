from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0048_restore_owner_email_sender"),
    ]

    operations = [
        migrations.AddField(
            model_name="portfolioproject",
            name="source_url",
            field=models.URLField(
                blank=True,
                default="",
                help_text="Ссылка на исходную публикацию, если кейс импортирован.",
                verbose_name="Источник",
            ),
        ),
    ]
