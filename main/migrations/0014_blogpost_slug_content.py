from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_service_calculator_profiles'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='slug',
            field=models.SlugField(
                blank=True,
                max_length=220,
                verbose_name='Слаг (URL)',
                help_text='Заполняется автоматически из заголовка. Используется для /blog/<slug>/',
            ),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='content',
            field=models.TextField(
                blank=True,
                verbose_name='Текст статьи',
                help_text='Полный текст статьи (поддерживает HTML). Если заполнен — статья открывается на сайте.',
            ),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='url',
            field=models.URLField(
                blank=True,
                verbose_name='Внешняя ссылка',
                help_text='Заполните, если статья на внешнем сайте. Если пусто — используется внутренняя страница /blog/<slug>/',
            ),
        ),
        migrations.AlterField(
            model_name='blogsection',
            name='archive_url',
            field=models.CharField(
                max_length=255,
                default='/blog/',
                verbose_name='Ссылка «Все статьи»',
                help_text='Например /blog/ для внутреннего блога',
            ),
        ),
        # Make slug unique after adding (with blank=True for existing rows)
        migrations.AlterField(
            model_name='blogpost',
            name='slug',
            field=models.SlugField(
                blank=True,
                max_length=220,
                verbose_name='Слаг (URL)',
            ),
        ),
    ]
