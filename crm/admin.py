import json

from django.contrib import admin
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline

from .models import (
    CrmActivity,
    CrmContact,
    CrmDeal,
    CrmLeadSource,
    CrmPipeline,
    CrmStage,
    CrmTag,
    CrmTask,
)
from .services import ensure_crm_defaults


class CrmTaskInline(TabularInline):
    model = CrmTask
    extra = 0
    fields = ("title", "due_at", "assigned_to", "is_done")
    autocomplete_fields = ("assigned_to",)


class CrmActivityInline(TabularInline):
    model = CrmActivity
    extra = 0
    fields = ("activity_type", "body", "author", "created_at")
    readonly_fields = ("created_at",)
    autocomplete_fields = ("author",)


class CrmStageInline(TabularInline):
    model = CrmStage
    extra = 0
    fields = ("name", "sort_order", "color", "stage_type")


@admin.register(CrmPipeline)
class CrmPipelineAdmin(ModelAdmin):
    list_display = ("name", "slug", "is_default", "is_active", "sort_order", "stage_count")
    list_editable = ("is_default", "is_active", "sort_order")
    prepopulated_fields = {"slug": ("name",)}
    inlines = (CrmStageInline,)

    @admin.display(description="Этапов")
    def stage_count(self, obj):
        return obj.stages.count()



@admin.register(CrmStage)
class CrmStageAdmin(ModelAdmin):
    list_display = ("name", "pipeline", "sort_order", "stage_type", "color_preview", "deals_count")
    list_filter = ("pipeline", "stage_type")
    list_editable = ("sort_order",)
    ordering = ("pipeline", "sort_order")

    @admin.display(description="Цвет")
    def color_preview(self, obj):
        return format_html(
            '<span style="display:inline-block;width:14px;height:14px;border-radius:3px;background:{}"></span> {}',
            obj.color,
            obj.color,
        )

    @admin.display(description="Сделок")
    def deals_count(self, obj):
        return obj.deals.count()


@admin.register(CrmLeadSource)
class CrmLeadSourceAdmin(ModelAdmin):
    list_display = ("name", "code", "is_active", "sort_order")
    list_editable = ("is_active", "sort_order")
    search_fields = ("name", "code")


@admin.register(CrmTag)
class CrmTagAdmin(ModelAdmin):
    list_display = ("name", "color")


@admin.register(CrmContact)
class CrmContactAdmin(ModelAdmin):
    list_display = ("name", "phone", "email", "company_name", "deals_count", "updated_at")
    search_fields = ("name", "phone", "email", "company_name")
    list_filter = ("created_at",)
    readonly_fields = ("created_at", "updated_at")

    @admin.display(description="Сделок")
    def deals_count(self, obj):
        return obj.deals.count()


@admin.register(CrmDeal)
class CrmDealAdmin(ModelAdmin):
    list_display = (
        "title",
        "contact",
        "stage",
        "responsible",
        "amount",
        "priority",
        "source",
        "updated_at",
    )
    list_filter = ("pipeline", "stage", "priority", "source", "responsible")
    search_fields = ("title", "contact__name", "contact__phone", "description")
    autocomplete_fields = ("contact", "responsible", "source")
    filter_horizontal = ("tags",)
    readonly_fields = ("created_at", "updated_at", "closed_at", "site_lead")
    inlines = (CrmTaskInline, CrmActivityInline)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    ("pipeline", "stage"),
                    "contact",
                    "responsible",
                    ("source", "priority"),
                    "tags",
                    "amount",
                    "description",
                    "lost_reason",
                    "site_lead",
                ),
            },
        ),
        (
            "Даты",
            {"fields": (("created_at", "updated_at", "closed_at"),), "classes": ("collapse",)},
        ),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                "kanban/",
                self.admin_site.admin_view(self.kanban_view),
                name="crm_crmdeal_kanban",
            ),
            path(
                "kanban/move/",
                self.admin_site.admin_view(self.kanban_move_view),
                name="crm_crmdeal_kanban_move",
            ),
        ]
        return custom + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["kanban_url"] = reverse("admin:crm_crmdeal_kanban")
        return super().changelist_view(request, extra_context)

    def kanban_view(self, request):
        ensure_crm_defaults()
        pipeline_id = request.GET.get("pipeline")
        pipelines = CrmPipeline.objects.filter(is_active=True).order_by("sort_order")
        if pipeline_id:
            pipeline = get_object_or_404(pipelines, pk=pipeline_id)
        else:
            pipeline = pipelines.filter(is_default=True).first() or pipelines.first()

        columns = []
        if pipeline:
            deals_qs = (
                CrmDeal.objects.filter(pipeline=pipeline)
                .select_related("contact", "responsible", "source", "stage")
                .prefetch_related("tags")
            )
            for stage in pipeline.stages.order_by("sort_order"):
                stage_deals = [d for d in deals_qs if d.stage_id == stage.id]
                total = sum((d.amount or 0) for d in stage_deals)
                columns.append(
                    {
                        "stage": stage,
                        "deals": stage_deals,
                        "count": len(stage_deals),
                        "total": total,
                    }
                )

        context = {
            **self.admin_site.each_context(request),
            "title": "Воронка продаж",
            "opts": self.model._meta,
            "pipelines": pipelines,
            "pipeline": pipeline,
            "columns": columns,
            "move_url": reverse("admin:crm_crmdeal_kanban_move"),
        }
        return TemplateResponse(request, "admin/crm/deal_kanban.html", context)

    def kanban_move_view(self, request):
        if request.method != "POST":
            return HttpResponseBadRequest("POST only")

        try:
            payload = json.loads(request.body.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return HttpResponseBadRequest("Invalid JSON")

        deal_id = payload.get("deal_id")
        stage_id = payload.get("stage_id")
        if not deal_id or not stage_id:
            return HttpResponseBadRequest("deal_id and stage_id required")

        deal = get_object_or_404(CrmDeal, pk=deal_id)
        stage = get_object_or_404(CrmStage, pk=stage_id)
        try:
            deal.move_to_stage(stage, user=request.user)
        except ValueError as exc:
            return JsonResponse({"ok": False, "error": str(exc)}, status=400)

        return JsonResponse(
            {
                "ok": True,
                "deal_id": deal.pk,
                "stage_id": stage.pk,
                "stage_name": stage.name,
                "is_closed": deal.is_closed,
            }
        )

    def save_model(self, request, obj, form, change):
        obj._stage_change_user = request.user
        super().save_model(request, obj, form, change)


@admin.register(CrmTask)
class CrmTaskAdmin(ModelAdmin):
    list_display = ("title", "deal", "due_at", "assigned_to", "is_done", "created_at")
    list_filter = ("is_done", "assigned_to", "due_at")
    search_fields = ("title", "deal__title")
    autocomplete_fields = ("deal", "assigned_to")


@admin.register(CrmActivity)
class CrmActivityAdmin(ModelAdmin):
    list_display = ("deal", "activity_type", "author", "created_at", "body_preview")
    list_filter = ("activity_type", "created_at")
    search_fields = ("body", "deal__title")
    autocomplete_fields = ("deal", "author")

    @admin.display(description="Текст")
    def body_preview(self, obj):
        return obj.body[:80] + ("…" if len(obj.body) > 80 else "")
