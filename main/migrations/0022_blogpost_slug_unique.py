from django.db import migrations, models
from django.utils.text import slugify


def fill_empty_slugs(apps, schema_editor):
    BlogPost = apps.get_model("main", "BlogPost")
    for post in BlogPost.objects.order_by("pk"):
        if (post.slug or "").strip():
            continue
        base = (slugify(post.title) or "post")[:180]
        candidate = base
        n = 2
        while BlogPost.objects.filter(slug=candidate).exclude(pk=post.pk).exists():
            candidate = f"{base}-{n}"
            n += 1
        post.slug = candidate
        post.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0021_home_quiz_settings"),
    ]

    operations = [
        migrations.RunPython(fill_empty_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="blogpost",
            name="slug",
            field=models.SlugField(
                blank=True,
                help_text="Заполняется автоматически из заголовка. Используется для /blog/<slug>/",
                max_length=220,
                unique=True,
                verbose_name="Слаг (URL)",
            ),
        ),
    ]
