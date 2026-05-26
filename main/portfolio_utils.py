"""Порядок фото в кейсе: sort_order 0 = обложка на карточке."""

from django.templatetags.static import static
from django.utils.html import format_html


def portfolio_admin_thumb(obj, *, width=72, height=48, border="1px solid #333"):
    """Превью для админки: загрузка (media) или демо-файл из static/."""
    if obj is None:
        return None
    img_style = (
        "display:block;width:{}px;height:{}px;object-fit:cover;"
        "border-radius:6px;border:{}"
    )
    if getattr(obj, "image", None):
        return format_html(
            '<img src="{}" alt="" style="{}" />',
            obj.image.url,
            img_style.format(width, height, border),
        )
    path = getattr(obj, "static_image", None) or ""
    if path:
        return format_html(
            '<img src="{}" alt="" style="{}" />',
            static(path),
            img_style.format(width, height, border),
        )
    return None


def sync_portfolio_photo_order(project):
    photos = list(project.photos.filter(is_active=True).order_by("sort_order", "pk"))
    for index, photo in enumerate(photos):
        updates = {}
        if photo.sort_order != index:
            updates["sort_order"] = index
        if photo.is_cover != (index == 0):
            updates["is_cover"] = index == 0
        if updates:
            type(photo).objects.filter(pk=photo.pk).update(**updates)


def migrate_legacy_project_cover(project, PortfolioProjectImage):
    """Переносит обложку с полей кейса в галерею, если строк фото ещё нет."""
    if project.photos.exists():
        return
    if not project.image and not project.static_image:
        return
    PortfolioProjectImage.objects.create(
        project=project,
        image=project.image,
        static_image=project.static_image or "",
        sort_order=0,
        is_cover=True,
        is_active=True,
    )
