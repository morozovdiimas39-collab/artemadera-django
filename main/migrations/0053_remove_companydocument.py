from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0052_restore_work_process_add_separate_how_we_work"),
    ]

    operations = [
        migrations.DeleteModel(
            name="CompanyDocument",
        ),
    ]
