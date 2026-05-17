from django.contrib import admin
from django.db.utils import OperationalError
from unfold.admin import ModelAdmin
from django.utils.html import format_html
from .models import (
    Service,
    CalculatorConfig,
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
    FaqSection,
    FaqItem,
    BeforeAfterSection,
    BeforeAfterItem,
    BlogSection,
    BlogPost,
)


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'price_from', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(CalculatorConfig)
class CalculatorConfigAdmin(ModelAdmin):
    list_display = ('area_min', 'area_max', 'area_step', 'area_default')

    def has_add_permission(self, request):
        try:
            return not CalculatorConfig.objects.exists()
        except OperationalError:
            return True

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(CalculatorMaterial)
class CalculatorMaterialAdmin(ModelAdmin):
    list_display = ('label', 'key', 'price_per_sqm', 'sort_order', 'is_active')
    list_editable = ('price_per_sqm', 'sort_order', 'is_active')
    search_fields = ('label', 'key')
    ordering = ('sort_order', 'pk')


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
    list_display = ('name', 'slug', 'unit_type', 'show_service_picker', 'is_active', 'sort_order')
    list_editable = ('is_active', 'sort_order')
    list_filter = ('unit_type', 'show_service_picker', 'is_active')
    search_fields = ('name', 'slug', 'title')
    prepopulated_fields = {'slug': ('name',)}
    inlines = (CalculatorOptionInline, CalculatorServiceChoiceInline)
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'name',
                    'slug',
                    'is_active',
                    'sort_order',
                    'show_service_picker',
                )
            },
        ),
        (
            'Тексты блока',
            {
                'fields': (
                    'badge_text',
                    'title',
                    'description',
                    'perk_1',
                    'perk_2',
                    'perk_3',
                    'submit_button_text',
                )
            },
        ),
        (
            'Расчёт',
            {
                'fields': (
                    'unit_type',
                    'unit_label',
                    'options_label',
                    'area_min',
                    'area_max',
                    'area_step',
                    'area_default',
                )
            },
        ),
    )


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


class PortfolioProjectImageInline(admin.TabularInline):
    model = PortfolioProjectImage
    extra = 1
    fields = ("image", "static_image", "caption", "is_cover", "sort_order", "is_active")
    ordering = ("-is_cover", "sort_order", "pk")


@admin.register(PortfolioProject)
class PortfolioProjectAdmin(ModelAdmin):
    list_display = ("preview", "title", "house_type", "location", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    list_filter = ("is_active", "house_type", "has_before_after")
    search_fields = ("title", "summary", "location", "work_types")
    ordering = ("sort_order", "pk")
    inlines = (PortfolioProjectImageInline,)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "summary",
                    "description",
                    ("house_type", "location"),
                    "work_types",
                    "has_before_after",
                    ("sort_order", "is_active"),
                )
            },
        ),
        (
            "Обложка (если без галереи)",
            {
                "fields": ("image", "static_image", "alt_text"),
                "classes": ("collapse",),
            },
        ),
    )

    @admin.display(description="Превью")
    def preview(self, obj):
        cover = obj.cover_item()
        if cover and getattr(cover, "image", None):
            return format_html(
                '<img src="{}" style="height:48px;width:72px;object-fit:cover;border-radius:6px"/>',
                cover.image.url,
            )
        if cover and getattr(cover, "static_image", None):
            return format_html(
                '<span style="font-size:11px;color:#888">static/</span>{}',
                cover.static_image[:24],
            )
        if obj.static_image:
            return format_html('<span style="font-size:11px">{}</span>', obj.static_image[:24])
        return "—"


@admin.register(ExperienceSection)
class ExperienceSectionAdmin(ModelAdmin):
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
                    "story",
                    "image",
                    "static_image",
                )
            },
        ),
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
    list_filter = ("icon", "is_active")
    search_fields = ("title", "description")
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
    search_fields = ("title", "description")
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


@admin.register(BeforeAfterItem)
class BeforeAfterItemAdmin(ModelAdmin):
    list_display = ("title", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    search_fields = ("title",)
    ordering = ("sort_order", "pk")
    fieldsets = (
        (None, {"fields": ("title", "sort_order", "is_active")}),
        (
            "Изображения",
            {
                "fields": (
                    ("before_image", "after_image"),
                    ("before_static", "after_static"),
                ),
                "description": "Загрузите фото или укажите путь в static, например images/before.jpg",
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
    list_display = ("preview", "title", "published_at", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "excerpt", "url")
    ordering = ("sort_order", "-published_at", "pk")
    fields = (
        "title",
        "excerpt",
        "url",
        ("image", "static_image"),
        "published_at",
        ("sort_order", "is_active"),
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
    list_display = ("name", "phone", "crm_deal_link", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "phone", "message")
    readonly_fields = ("created_at", "crm_deal_link")
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
