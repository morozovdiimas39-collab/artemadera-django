from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import models

from main.image_optimization import optimize_field_file


class Command(BaseCommand):
    help = "Converts uploaded ImageField files to resized WebP files and updates DB paths."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Show candidates without writing files.")

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        scanned = 0
        changed = 0

        for model in apps.get_models():
            image_fields = [
                field for field in model._meta.fields if isinstance(field, models.ImageField)
            ]
            if not image_fields:
                continue

            for obj in model.objects.all().iterator():
                updates = {}
                for field in image_fields:
                    field_file = getattr(obj, field.name, None)
                    if not field_file or not getattr(field_file, "name", ""):
                        continue
                    scanned += 1
                    if dry_run:
                        self.stdout.write(f"{model.__name__}.{field.name}: {field_file.name}")
                        continue
                    optimized_name = optimize_field_file(field_file)
                    if optimized_name and optimized_name != field_file.name:
                        updates[field.name] = optimized_name

                if updates:
                    model.objects.filter(pk=obj.pk).update(**updates)
                    changed += len(updates)
                    self.stdout.write(
                        self.style.SUCCESS(f"{model.__name__} #{obj.pk}: {updates}")
                    )

        if dry_run:
            self.stdout.write(self.style.WARNING(f"Found {scanned} image fields."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Optimized {changed} of {scanned} image fields."))
