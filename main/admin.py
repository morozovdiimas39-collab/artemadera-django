from django.contrib import admin
from django.db import models
from django.db.utils import OperationalError
from django.shortcuts import redirect
from django.urls import reverse
from unfold import widgets as unfold_widgets
from unfold.admin import ModelAdmin
from django.utils.html import format_html
from .forms import SitePageAdminForm
from .portfolio_utils import (
    migrate_legacy_project_cover,
    portfolio_admin_thumb,
    sync_portfolio_photo_order,
)
from .models import (
    Service,
    CalculatorConfig,
    HomeQuizSettings,
    CalculatorMaterial,
    CalculatorProfile,
    CalculatorOption,
    CalculatorServiceChoice,
    PortfolioSection,
    PortfolioProject,
    PortfolioProjectImage,
    ExperienceSection,
    ExperienceStat,
    ExperienceAdvantage,
    ReviewsSection,
    Review,
    WorkProcessSection,
    WorkProcessStep,
    ContactSection,
    ContactLead,
    LeadEmailSettings,
    FaqSection,
    FaqItem,
    BeforeAfterSection,
    BeforeAfterItem,
    BlogSection,
    BlogPost,
    SitePage,
    PageServiceLink,
)


class PageServiceLinkInline(admin.TabularInline):
    model = PageServiceLink
    extra = 1
    # Не используем autocomplete_fields: Select2 в табличном инлайне + Unfold даёт
    # «Совпадений не найдено» и сломанную вёрстку. Обычный select от Unfold — надёжно.
    fields = ("service", "sort_order", "layout", "tag_override", "cta_label", "is_visible")
    ordering = ("sort_order", "pk")


@admin.register(SitePage)
class SitePageAdmin(ModelAdmin):
    form = SitePageAdminForm
    formfield_overrides = {
        models.ImageField: {
            "widget": unfold_widgets.UnfoldAdminImageFieldWidget(
                attrs={"accept": "image/*"},
            ),
        },
    }
    list_display = ("title", "page_key", "url_link", "hero_preview", "services_count", "is_active")
    list_editable = ("is_active",)
    list_filter = ("is_active", "show_services_block")
    search_fields = ("title", "page_key")
    ordering = ("sort_order", "title")
    inlines = (PageServiceLinkInline,)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ("hero_image_preview",)
        return ()

    def get_fieldsets(self, request, obj=None):
        hero_fields = ["hero_image_preview", "hero_image"] if obj else ["hero_image"]
        return (
            (
                "Страница",
                {
                    "fields": (
                        ("title", "page_key"),
                        ("is_active", "sort_order"),
                        "show_services_block",
                    ),
                    "description": (
                        "URL без слэша в начале: home — главная, obsada/okna — страница окон. "
                        "Внизу добавляйте услуги из справочника."
                    ),
                },
            ),
            (
                "Фон первого экрана",
                {
                    "fields": tuple(hero_fields),
                    "description": (
                        "Загрузите картинку кнопкой справа от поля (иконка со стрелкой вверх). "
                        "После выбора файла нажмите «Сохранить» внизу — иначе фон не применится."
                    ),
                },
            ),
            (
                "Тексты первого экрана",
                {
                    "fields": (("hero_h1_white", "hero_h1_accent"), "hero_lead"),
                },
            ),
            (
                "Блок услуг на странице",
                {
                    "fields": (
                        "services_badge",
                        ("services_title_white", "services_title_accent"),
                        "services_lead",
                    ),
                    "description": (
                        "Тексты шапки блока карточек. На главной — при включённом «Показывать блок услуг». "
                        "На внутренних страницах — над сеткой в стиле страницы «Шлифовка»; в сетку попадают "
                        "только услуги из таблицы «Услуги на странице» ниже (порядок — колонка «Порядок»). "
                        "Если таблица пуста, страница использует свой старый статичный блок."
                    ),
                },
            ),
            (
                "Запасной фон (без загрузки)",
                {
                    "fields": ("hero_static_image",),
                    "classes": ("collapse",),
                    "description": "Путь к файлу в static/, если не загружаете картинку выше.",
                },
            ),
        )

    @admin.display(description="Текущий фон на сайте")
    def hero_image_preview(self, obj):
        if obj.hero_image:
            return format_html(
                '<div style="margin-bottom:12px">'
                '<img src="{}" alt="" style="display:block;max-width:min(100%,560px);'
                'max-height:280px;object-fit:cover;border-radius:12px;border:1px solid #333" />'
                '<p style="margin:8px 0 0;font-size:13px;color:#888">'
                "Чтобы заменить — выберите новый файл ниже и нажмите «Сохранить».</p></div>",
                obj.hero_image.url,
            )
        return format_html(
            '<p style="color:#888;font-size:13px;margin:0 0 12px">'
            "Фон ещё не загружен — используется запасной из static. "
            "Выберите файл в поле ниже.</p>"
        )

    @admin.display(description="URL")
    def url_link(self, obj):
        return format_html('<a href="{}" target="_blank">{}</a>', obj.url_path, obj.url_path)

    @admin.display(description="Фон")
    def hero_preview(self, obj):
        if obj.hero_image:
            return format_html(
                '<img src="{}" style="height:40px;width:72px;object-fit:cover;border-radius:4px" />',
                obj.hero_image.url,
            )
        return "—"

    @admin.display(description="Услуг")
    def services_count(self, obj):
        return obj.service_links.filter(is_visible=True).count()


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    """Общий справочник услуг — привязка к страницам в разделе «Страницы»."""

    formfield_overrides = {
        models.ImageField: {
            "widget": unfold_widgets.UnfoldAdminImageFieldWidget(
                attrs={"accept": "image/*"},
            ),
        },
    }
    list_display = ("name", "slug", "service_image_thumb", "catalog_tag", "page_url", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "slug", "short_description")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("calculator_profile",)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ("service_image_preview",)
        return ()

    def get_fieldsets(self, request, obj=None):
        image_fields = (
            ("service_image_preview", "image", "static_image")
            if obj
            else ("image", "static_image")
        )
        return (
        (
            None,
            {
                "fields": (
                    ("name", "slug"),
                    ("page_url", "order"),
                    "is_active",
                    "short_description",
                    image_fields,
                    "calculator_profile",
                ),
                "description": (
                    "Карточки на страницах настраиваются в «Страницы» → выберите страницу → "
                    "добавьте услугу из этого справочника. "
                    "Фото карточки: выберите файл в поле «Фото на главной» и нажмите «Сохранить»."
                ),
            },
        ),
        (
            "Дополнительно",
            {
                "fields": ("price_from", "description", "icon", "home_tag_override"),
                "classes": ("collapse",),
                "description": "home_tag_override — запасной бейдж, если не задан на странице.",
            },
        ),
        (
            "Устаревшее (главная)",
            {
                "fields": ("show_on_homepage", "home_layout"),
                "classes": ("collapse",),
                "description": "Не используется — настройте главную в «Страницы» → Главная.",
            },
        ),
    )

    @admin.display(description="Фото")
    def service_image_thumb(self, obj):
        thumb = portfolio_admin_thumb(obj)
        return thumb or "—"

    @admin.display(description="Текущее фото")
    def service_image_preview(self, obj):
        if obj.image:
            return format_html(
                '<div style="margin-bottom:12px">'
                '<img src="{}" alt="" style="display:block;max-width:min(100%,400px);'
                'max-height:200px;object-fit:cover;border-radius:12px;border:1px solid #333" />'
                '<p style="margin:8px 0 0;font-size:13px;color:#888">'
                "Чтобы заменить — выберите новый файл ниже и нажмите «Сохранить».</p></div>",
                obj.image.url,
            )
        if obj.static_image:
            return format_html(
                '<p style="color:#888;font-size:13px;margin:0 0 12px">'
                "Сейчас используется картинка из static (поле ниже). "
                "Загрузите файл в «Фото на главной», чтобы перейти на свою картинку.</p>"
            )
        return format_html(
            '<p style="color:#888;font-size:13px;margin:0 0 12px">'
            "Фото ещё не загружено — выберите файл в поле «Фото на главной» ниже.</p>"
        )

    @admin.display(description="Бейдж")
    def catalog_tag(self, obj):
        return obj.get_home_tag() or "—"


class CalculatorConfigAdmin(ModelAdmin):
    list_display = ("area_min", "area_max", "area_step", "area_default")

    def has_add_permission(self, request):
        try:
            return not CalculatorConfig.objects.exists()
        except OperationalError:
            return True

    def has_delete_permission(self, request, obj=None):
        return False


class HomeQuizSettingsAdmin(ModelAdmin):
    list_display = ("__str__",)

    formfield_overrides = {
        models.ImageField: {
            "widget": unfold_widgets.UnfoldAdminImageFieldWidget(
                attrs={"accept": "image/*"},
            ),
        },
    }

    fieldsets = (
        (
            None,
            {
                "fields": ("default_image",),
                "description": (
                    "Большое фото справа в блоке «Рассчитайте стоимость работ». "
                    "Пустые поля — как раньше, изображения из папки static сайта."
                ),
            },
        ),
        (
            "По кнопкам шага «Что нужно сделать?»",
            {
                "fields": (
                    ("image_shlifovka", "image_pokraska", "image_teplyy_shov"),
                    ("image_okosyachka", "image_obsada", "image_kryshi"),
                    ("image_injeneriya",),
                ),
            },
        ),
    )

    def has_add_permission(self, request):
        try:
            return not HomeQuizSettings.objects.exists()
        except OperationalError:
            return True

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        try:
            if HomeQuizSettings.objects.filter(pk=1).exists():
                return redirect(
                    reverse("admin:main_homequizsettings_change", args=(1,))
                )
        except OperationalError:
            pass
        return super().changelist_view(request, extra_context=extra_context)


class CalculatorMaterialAdmin(ModelAdmin):
    """Старый справочник — не показываем в меню, только прямой URL."""
    list_display = ("label", "key", "price_per_sqm", "sort_order", "is_active")
    list_editable = ("price_per_sqm", "sort_order", "is_active")
    search_fields = ("label", "key")
    ordering = ("sort_order", "pk")


class CalculatorOptionInline(admin.TabularInline):
    model = CalculatorOption
    extra = 0
    fields = ('label', 'key', 'price_per_unit', 'sort_order', 'is_active')
    ordering = ('sort_order', 'pk')


class CalculatorServiceChoiceInline(admin.TabularInline):
    model = CalculatorServiceChoice
    fk_name = 'profile'
    extra = 0
    fields = ('label', 'target_profile', 'hint', 'sort_order', 'is_active')
    ordering = ('sort_order', 'pk')
    autocomplete_fields = ('target_profile',)


@admin.register(CalculatorProfile)
class CalculatorProfileAdmin(ModelAdmin):
    list_display = ("name", "slug", "unit_type", "min_price_preview", "is_active", "sort_order")
    list_editable = ("is_active", "sort_order")
    list_filter = ("unit_type", "is_active")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    inlines = (CalculatorOptionInline, CalculatorServiceChoiceInline)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("name", "slug"),
                    ("is_active", "sort_order"),
                    "show_service_picker",
                    ("unit_type", "unit_label"),
                    "options_label",
                    ("area_min", "area_max"),
                    ("area_step", "area_default"),
                )
            },
        ),
        (
            "Тексты на странице",
            {
                "classes": ("collapse",),
                "fields": (
                    "badge_text",
                    "title",
                    "description",
                    "perk_1",
                    "perk_2",
                    "perk_3",
                    "submit_button_text",
                ),
            },
        ),
    )

    @admin.display(description="от")
    def min_price_preview(self, obj):
        return obj.home_price_tag() or "—"


@admin.register(PortfolioSection)
class PortfolioSectionAdmin(ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "is_visible",
                    "badge_text",
                    "title_prefix",
                    "title_highlight",
                    "description",
                )
            },
        ),
    )

    def has_add_permission(self, request):
        try:
            return not PortfolioSection.objects.exists()
        except OperationalError:
            return True

    def has_delete_permission(self, request, obj=None):
        return False


_PORTFOLIO_IMAGE_WIDGET = {
    models.ImageField: {
        "widget": unfold_widgets.UnfoldAdminImageFieldWidget(
            attrs={"accept": "image/*"},
        ),
    },
}


class PortfolioProjectImageInline(admin.TabularInline):
    model = PortfolioProjectImage
    extra = 1
    min_num = 0
    fields = ("photo_thumb", "image", "sort_order", "caption")
    readonly_fields = ("photo_thumb",)
    ordering = ("sort_order", "pk")
    formfield_overrides = _PORTFOLIO_IMAGE_WIDGET
    classes = ("wide", "portfolio-photo-inline",)
    verbose_name = "Фото"
    verbose_name_plural = "Фото кейса"

    @admin.display(description="")
    def photo_thumb(self, obj):
        thumb = portfolio_admin_thumb(obj)
        return thumb or "—"


@admin.register(PortfolioProject)
class PortfolioProjectAdmin(ModelAdmin):
    list_display = ("preview", "admin_title", "photos_count", "house_type", "location", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    list_filter = ("is_active", "house_type", "has_before_after")
    search_fields = ("title", "summary", "location", "work_types")
    ordering = ("sort_order", "pk")
    inlines = (PortfolioProjectImageInline,)

    def get_fieldsets(self, request, obj=None):
        blocks = [
            (
                None,
                {
                    "fields": (
                        "title",
                        ("sort_order", "is_active"),
                    ),
                    "description": (
                        "Минимум для публикации — одна фотография в таблице ниже. "
                        "Название, описание, тип дома, область и услуги можно не заполнять."
                    ),
                },
            ),
            (
                "Подписи и детали",
                {
                    "fields": (
                        "summary",
                        "description",
                        ("house_type", "location"),
                        "work_types",
                        "has_before_after",
                    ),
                    "classes": ("collapse",),
                },
            ),
        ]
        if obj:
            blocks.append(
                (
                    "Фото проекта",
                    {
                        "fields": ("gallery_preview",),
                        "description": (
                            "Фото с № 0 будет обложкой. Если есть только одно фото — этого достаточно. "
                            "Если фото несколько, они появятся в галерее проекта."
                        ),
                    },
                )
            )
        return blocks

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ("gallery_preview",)
        return ()

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        migrate_legacy_project_cover(form.instance, PortfolioProjectImage)
        sync_portfolio_photo_order(form.instance)

    def save_formset(self, request, form, formset, change):
        if formset.model is not PortfolioProjectImage:
            super().save_formset(request, form, formset, change)
            return
        if not formset.is_valid():
            super().save_formset(request, form, formset, change)
            return

        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            if not instance.image and not instance.static_image and not instance.pk:
                continue
            instance.is_active = True
            instance.project = form.instance
            instance.save()
        formset.save_m2m()

    @admin.display(description="Как на сайте")
    def gallery_preview(self, obj):
        items = obj.get_gallery_items()
        if not items:
            return format_html(
                '<p style="margin:0;color:#888;font-size:13px">'
                "Пока нет фото — добавьте в таблице ниже.</p>"
            )
        parts = [
            '<div style="display:flex;flex-wrap:wrap;gap:10px;align-items:flex-end">'
        ]
        for index, photo in enumerate(items):
            label = "Обложка" if index == 0 else f"№{index}"
            border = "2px solid #f59e0b" if index == 0 else "1px solid #333"
            thumb = portfolio_admin_thumb(photo, width=96, height=64, border=border)
            if thumb:
                parts.append(
                    format_html(
                        '<figure style="margin:0;text-align:center">{}'
                        '<figcaption style="margin-top:4px;font-size:11px;color:#aaa">{}</figcaption>'
                        "</figure>",
                        thumb,
                        label,
                    )
                )
        parts.append("</div>")
        return format_html("".join(str(p) for p in parts))

    @admin.display(description="Фото")
    def photos_count(self, obj):
        n = obj.photos.filter(is_active=True).count()
        return n or "—"

    @admin.display(description="Проект")
    def admin_title(self, obj):
        return obj.display_title

    @admin.display(description="Превью")
    def preview(self, obj):
        cover = obj.cover_item()
        return portfolio_admin_thumb(cover) or "—"


@admin.register(ExperienceSection)
class ExperienceSectionAdmin(ModelAdmin):
    formfield_overrides = {
        models.ImageField: {
            "widget": unfold_widgets.UnfoldAdminImageFieldWidget(
                attrs={"accept": "image/*"},
            ),
        },
    }
    readonly_fields = ("experience_cover_preview",)

    def get_fieldsets(self, request, obj=None):
        # Отдельные строки: кортеж (a, b, c) в fields = одна строка из трёх колонок.
        if obj:
            photo_fields = (
                "experience_cover_preview",
                "image",
                "static_image",
            )
        else:
            photo_fields = ("image", "static_image")
        return (
            (
                None,
                {
                    "fields": (
                        "is_visible",
                        ("badge_text",),
                        ("title_prefix", "title_highlight"),
                        "description",
                        "story",
                    )
                },
            ),
            (
                "Фото справа в блоке",
                {
                    "description": (
                        "Если «Фото (загрузка)» пусто — на сайте показывается файл из каталога "
                        "<code>static/</code>. Укажите путь относительно него, например "
                        "<code>images/team.png</code>."
                    ),
                    "fields": photo_fields,
                },
            ),
        )

    @admin.display(description="Сейчас на сайте")
    def experience_cover_preview(self, obj):
        thumb = portfolio_admin_thumb(obj, width=280, height=175)
        if thumb:
            return format_html(
                '<div style="margin-bottom:8px">{}'
                '<p style="margin:8px 0 0;font-size:12px;color:#888">'
                "Превью: загрузка имеет приоритет над путём к static.</p></div>",
                thumb,
            )
        return format_html(
            '<p style="color:#888;font-size:13px;margin:0">'
            "Нет загрузки и не задан путь к картинке в static.</p>"
        )

    def has_add_permission(self, request):
        try:
            return not ExperienceSection.objects.exists()
        except OperationalError:
            return True

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ExperienceStat)
class ExperienceStatAdmin(ModelAdmin):
    list_display = ("value", "label", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    ordering = ("sort_order", "pk")


@admin.register(ExperienceAdvantage)
class ExperienceAdvantageAdmin(ModelAdmin):
    list_display = ("title", "icon", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    list_filter = ("icon",)
    search_fields = ("title",)
    ordering = ("sort_order", "pk")


@admin.register(ReviewsSection)
class ReviewsSectionAdmin(ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "is_visible",
                    "badge_text",
                    "title_prefix",
                    "title_highlight",
                    "description",
                    "yandex_rating",
                    "yandex_reviews_count",
                    "yandex_maps_url",
                )
            },
        ),
    )

    def has_add_permission(self, request):
        try:
            return not ReviewsSection.objects.exists()
        except OperationalError:
            return True

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ("author_name", "headline", "rating", "source", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active", "rating")
    list_filter = ("source", "is_active", "rating")
    search_fields = ("author_name", "headline", "text")
    ordering = ("sort_order", "pk")


@admin.register(WorkProcessSection)
class WorkProcessSectionAdmin(ModelAdmin):
    fields = (
        "is_visible",
        "badge_text",
        "title_prefix",
        "title_highlight",
        "description",
    )

    def has_add_permission(self, request):
        try:
            return not WorkProcessSection.objects.exists()
        except OperationalError:
            return True

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(WorkProcessStep)
class WorkProcessStepAdmin(ModelAdmin):
    list_display = ("step_number", "title", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    search_fields = ("title",)
    ordering = ("sort_order", "pk")


@admin.register(ContactSection)
class ContactSectionAdmin(ModelAdmin):
    fields = (
        "is_visible",
        "badge_text",
        "title_prefix",
        "title_highlight",
        "description",
        "phone",
        "phone_href",
        "email",
        "work_hours",
        "address",
        "submit_button_text",
        "privacy_note",
    )

    def has_add_permission(self, request):
        try:
            return not ContactSection.objects.exists()
        except OperationalError:
            return True

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(FaqSection)
class FaqSectionAdmin(ModelAdmin):
    fields = (
        "is_visible",
        "badge_text",
        "title_prefix",
        "title_highlight",
        "description",
    )

    def has_add_permission(self, request):
        try:
            return not FaqSection.objects.exists()
        except OperationalError:
            return True

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(FaqItem)
class FaqItemAdmin(ModelAdmin):
    list_display = ("question", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    search_fields = ("question", "answer")
    ordering = ("sort_order", "pk")


@admin.register(BeforeAfterSection)
class BeforeAfterSectionAdmin(ModelAdmin):
    fields = (
        "is_visible",
        "badge_text",
        "title_prefix",
        "title_highlight",
        "description",
    )

    def has_add_permission(self, request):
        try:
            return not BeforeAfterSection.objects.exists()
        except OperationalError:
            return True

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        try:
            if BeforeAfterSection.objects.filter(pk=1).exists():
                return redirect(
                    reverse("admin:main_beforeaftersection_change", args=(1,))
                )
        except OperationalError:
            pass
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(BeforeAfterItem)
class BeforeAfterItemAdmin(ModelAdmin):
    list_display = ("title", "page", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    list_filter = ("page", "is_active")
    search_fields = ("title", "page__title", "page__page_key")
    ordering = ("sort_order", "pk")
    formfield_overrides = {
        models.ImageField: {
            "widget": unfold_widgets.UnfoldAdminImageFieldWidget(
                attrs={"accept": "image/*"},
            ),
        },
    }
    fieldsets = (
        (
            None,
            {
                "fields": ("title", "page", "sort_order", "is_active"),
                "description": (
                    "Выберите страницу услуги, если это сравнение должно показываться только там. "
                    "Оставьте поле пустым для общего блока на всех страницах."
                ),
            },
        ),
        (
            "Фото для слайдера на сайте",
            {
                "description": (
                    "Загрузите «До» и «После». Если файл не загружен, подставится путь из блока "
                    "ниже (как запасной вариант из темы сайта)."
                ),
                "fields": (("before_image", "after_image"),),
            },
        ),
        (
            "Запас из static (если нет загрузки)",
            {
                "classes": ("collapse",),
                "fields": (("before_static", "after_static"),),
            },
        ),
    )


@admin.register(BlogSection)
class BlogSectionAdmin(ModelAdmin):
    fields = (
        "is_visible",
        "badge_text",
        "title_prefix",
        "title_highlight",
        "description",
        "archive_url",
        "archive_link_text",
    )

    def has_add_permission(self, request):
        try:
            return not BlogSection.objects.exists()
        except OperationalError:
            return True

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(BlogPost)
class BlogPostAdmin(ModelAdmin):
    list_display = ("preview", "title", "published_at", "is_active")
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    search_fields = ("title", "excerpt", "slug")
    ordering = ("sort_order", "-published_at", "pk")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("title", "slug"),
                    "excerpt",
                    "content",
                    ("image", "static_image"),
                    ("published_at", "is_active"),
                    "sort_order",
                )
            },
        ),
        (
            "Внешняя ссылка",
            {
                "classes": ("collapse",),
                "fields": ("url",),
                "description": "Оставьте пустым — статья на этом сайте: /blog/слаг/",
            },
        ),
    )

    @admin.display(description="Превью")
    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:40px;width:64px;object-fit:cover;border-radius:4px"/>',
                obj.image.url,
            )
        if obj.static_image:
            return format_html('<span style="font-size:11px">{}</span>', obj.static_image[:28])
        return "—"


@admin.register(ContactLead)
class ContactLeadAdmin(ModelAdmin):
    list_display = ("name", "phone", "direct_status", "ym_client_id", "crm_deal_link", "created_at")
    list_filter = ("direct_status", "created_at")
    search_fields = ("name", "phone", "message", "ym_client_id")
    readonly_fields = ("created_at", "direct_status_updated_at", "crm_deal_link")
    ordering = ("-created_at",)
    actions = ("create_crm_deals",)

    @admin.display(description="CRM")
    def crm_deal_link(self, obj):
        deal = getattr(obj, "crm_deal", None)
        if not deal:
            return "—"
        from django.urls import reverse

        url = reverse("admin:crm_crmdeal_change", args=[deal.pk])
        return format_html('<a href="{}">Сделка #{}</a>', url, deal.pk)

    @admin.action(description="Создать сделки в CRM")
    def create_crm_deals(self, request, queryset):
        from crm.services import create_deal_from_site_lead

        created = 0
        for lead in queryset:
            if hasattr(lead, "crm_deal") and lead.crm_deal_id:
                continue
            create_deal_from_site_lead(lead, user=request.user)
            created += 1
        self.message_user(request, f"Создано сделок: {created}")


@admin.register(LeadEmailSettings)
class LeadEmailSettingsAdmin(ModelAdmin):
    fieldsets = (
        (
            "Получатели",
            {
                "fields": ("notification_emails", "test_email_link"),
                "description": (
                    "Сюда — адреса, куда уходит письмо при каждой новой заявке "
                    "(все формы с кнопкой отправки на сайте). Пустое поле = письма не шлются."
                ),
            },
        ),
        (
            "SMTP",
            {
                "fields": (
                    "smtp_login",
                    "smtp_password",
                    ("smtp_host", "smtp_port"),
                    ("smtp_use_tls", "smtp_use_ssl"),
                ),
                "description": (
                    "Для Яндекса: логин почты + пароль приложения. Обычно host=smtp.yandex.ru, "
                    "port=587, TLS включён. Если 587 закрыт на хостинге — port=465, TLS выключить, SSL включить."
                ),
            },
        ),
    )
    readonly_fields = ("test_email_link",)

    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        custom = [
            path(
                "<path:object_id>/test-email/",
                self.admin_site.admin_view(self.test_email_view),
                name="main_leademailsettings_test_email",
            ),
        ]
        return custom + urls

    @admin.display(description="Проверка")
    def test_email_link(self, obj):
        if not obj or not obj.pk:
            return "Сначала сохраните настройки."
        from django.urls import reverse

        url = reverse("admin:main_leademailsettings_test_email", args=[obj.pk])
        return format_html(
            '<a class="button" href="{}" style="display:inline-flex;align-items:center;'
            'padding:8px 12px;border-radius:6px;background:#f59e0b;color:#111827;'
            'font-weight:700;text-decoration:none">Отправить тестовое письмо</a>',
            url,
        )

    def test_email_view(self, request, object_id):
        from django.contrib import messages
        from django.shortcuts import redirect
        from django.urls import reverse
        from .lead_notifications import send_lead_test_email

        try:
            sent_count = send_lead_test_email()
        except Exception as exc:
            messages.error(request, f"Тестовое письмо не отправлено: {type(exc).__name__}: {exc}")
        else:
            messages.success(request, f"Тестовое письмо отправлено. SMTP вернуло: {sent_count}.")
        return redirect(reverse("admin:main_leademailsettings_change", args=[object_id]))

    def changelist_view(self, request, extra_context=None):
        """Одна запись — сразу открываем форму с полем, а не пустой список."""
        from django.shortcuts import redirect
        from django.urls import reverse

        try:
            url = reverse("admin:main_leademailsettings_change", args=[1])
        except Exception:
            url = "/admin/main/leademailsettings/1/change/"
        return redirect(url)

    def has_add_permission(self, request):
        try:
            return not LeadEmailSettings.objects.exists()
        except OperationalError:
            return True

    def has_delete_permission(self, request, obj=None):
        return False


# Служебные модели — без пункта в боковом меню (только кастомная навигация Unfold)
admin.site.register(CalculatorConfig, CalculatorConfigAdmin)
admin.site.register(HomeQuizSettings, HomeQuizSettingsAdmin)
admin.site.register(CalculatorMaterial, CalculatorMaterialAdmin)
