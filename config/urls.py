"""
URL configuration for config project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve as static_serve
from django.views.generic import RedirectView

from main.direct_conversions import direct_conversions_csv_view
from main.views import (
    blog_detail,
    blog_list,
    generic_service,
    index,
    lead_direct_status,
    pokraska,
    shlifovka,
    robots_txt,
    sitemap_xml,
    teplyy_shov,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("sitemap.xml", sitemap_xml, name="sitemap_xml"),
    path("export/yandex-direct-conversions.csv", direct_conversions_csv_view, name="direct_conversions_csv"),
    path("lead-status/<path:token>/", lead_direct_status, name="lead_direct_status"),
    path("", index, name="index"),
    path("shlifovka", shlifovka, name="shlifovka"),
    path("shlifovka/", RedirectView.as_view(url="/shlifovka", permanent=True)),
    path("otdelka/shlifovka", RedirectView.as_view(url="/shlifovka", permanent=True)),
    path("otdelka/shlifovka/", RedirectView.as_view(url="/shlifovka", permanent=True)),
    path("pokraska", pokraska, name="pokraska"),
    path("pokraska/", pokraska),
    path("teplyy-shov", teplyy_shov, name="teplyy_shov"),
    path("teplyy-shov/", teplyy_shov),
    path("blog", blog_list),
    path("blog/", blog_list, name="blog_list"),
    path("blog/<slug:slug>/", blog_detail, name="blog_detail"),
]

# static и media — ДО catch-all, иначе /media/... уходит в generic_service
urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / "static")
if settings.DEBUG or getattr(settings, "SERVE_MEDIA", False):
    urlpatterns.append(
        re_path(r"^media/(?P<path>.*)$", static_serve, {"document_root": settings.MEDIA_ROOT})
    )

urlpatterns.append(path("<path:path>", generic_service, name="generic_service"))
