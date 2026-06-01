"""
URL configuration for config project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from main.direct_conversions import direct_conversions_csv_view
from main.views import (
    blog_detail,
    blog_list,
    generic_service,
    index,
    lead_direct_status,
    pokraska,
    shlifovka,
    teplyy_shov,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("export/yandex-direct-conversions.csv", direct_conversions_csv_view, name="direct_conversions_csv"),
    path("lead-status/<path:token>/", lead_direct_status, name="lead_direct_status"),
    path("", index, name="index"),
    path("shlifovka", shlifovka, name="shlifovka"),
    path("pokraska", pokraska, name="pokraska"),
    path("teplyy-shov", teplyy_shov, name="teplyy_shov"),
    path("blog/", blog_list, name="blog_list"),
    path("blog/<slug:slug>/", blog_detail, name="blog_detail"),
]

# static и media — ДО catch-all, иначе /media/... уходит в generic_service
urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / "static")
if settings.DEBUG or getattr(settings, "SERVE_MEDIA", False):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns.append(path("<path:path>", generic_service, name="generic_service"))
