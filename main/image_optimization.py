from io import BytesIO
from pathlib import PurePosixPath

from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, ImageOps, UnidentifiedImageError


MAX_IMAGE_SIDE = 1920
WEBP_QUALITY = 78


def _target_name(name):
    path = PurePosixPath(name)
    return str(path.with_suffix(".webp"))


def optimize_field_file(field_file, *, max_side=MAX_IMAGE_SIDE, quality=WEBP_QUALITY):
    if not field_file or not getattr(field_file, "name", ""):
        return None

    storage = field_file.storage
    original_name = field_file.name
    if not storage.exists(original_name):
        existing_target = _target_name(original_name)
        if existing_target != original_name and storage.exists(existing_target):
            return existing_target
        return None

    try:
        with storage.open(original_name, "rb") as source:
            image = Image.open(source)
            image = ImageOps.exif_transpose(image)
            image.load()
    except (OSError, UnidentifiedImageError, ValueError):
        return None

    if image.mode not in ("RGB", "RGBA"):
        image = image.convert("RGBA" if "A" in image.getbands() else "RGB")

    if max(image.size) > max_side:
        image.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)

    output = BytesIO()
    save_kwargs = {
        "format": "WEBP",
        "quality": quality,
        "method": 6,
    }
    if image.mode == "RGBA":
        save_kwargs["lossless"] = False
    else:
        image = image.convert("RGB")
    image.save(output, **save_kwargs)

    target_name = _target_name(original_name)
    if target_name == original_name and storage.exists(original_name):
        storage.delete(original_name)
    elif storage.exists(target_name):
        storage.delete(target_name)

    saved_name = storage.save(target_name, ContentFile(output.getvalue()))
    if original_name != saved_name and storage.exists(original_name):
        storage.delete(original_name)

    return saved_name


def optimize_instance_images(instance):
    updates = {}
    for field in instance._meta.fields:
        if not isinstance(field, models.ImageField):
            continue
        field_file = getattr(instance, field.name, None)
        optimized_name = optimize_field_file(field_file)
        if optimized_name and optimized_name != getattr(field_file, "name", ""):
            updates[field.name] = optimized_name

    if updates and instance.pk:
        type(instance).objects.filter(pk=instance.pk).update(**updates)
        for field_name, value in updates.items():
            setattr(instance, field_name, value)

    return updates
