from django.conf import settings
from django.db import models
from django.utils import timezone


class CrmPipeline(models.Model):
    name = models.CharField(max_length=120, verbose_name="Название")
    slug = models.SlugField(max_length=64, unique=True, verbose_name="Код")
    is_default = models.BooleanField(default=False, verbose_name="По умолчанию")
    sort_order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        verbose_name = "Воронка"
        verbose_name_plural = "Воронки"
        ordering = ["sort_order", "pk"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_default:
            CrmPipeline.objects.exclude(pk=self.pk).update(is_default=False)


class CrmStage(models.Model):
    TYPE_OPEN = "open"
    TYPE_WON = "won"
    TYPE_LOST = "lost"
    TYPE_CHOICES = [
        (TYPE_OPEN, "В работе"),
        (TYPE_WON, "Успех"),
        (TYPE_LOST, "Отказ"),
    ]

    pipeline = models.ForeignKey(
        CrmPipeline,
        on_delete=models.CASCADE,
        related_name="stages",
        verbose_name="Воронка",
    )
    name = models.CharField(max_length=120, verbose_name="Этап")
    sort_order = models.IntegerField(default=0, verbose_name="Порядок")
    color = models.CharField(
        max_length=7,
        default="#d97706",
        verbose_name="Цвет",
        help_text="HEX, например #d97706",
    )
    stage_type = models.CharField(
        max_length=8,
        choices=TYPE_CHOICES,
        default=TYPE_OPEN,
        verbose_name="Тип этапа",
    )

    class Meta:
        verbose_name = "Этап воронки"
        verbose_name_plural = "Этапы воронки"
        ordering = ["pipeline", "sort_order", "pk"]
        unique_together = [("pipeline", "name")]

    def __str__(self):
        return f"{self.pipeline.name} → {self.name}"


class CrmLeadSource(models.Model):
    name = models.CharField(max_length=120, verbose_name="Название")
    code = models.SlugField(max_length=32, unique=True, verbose_name="Код")
    sort_order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Источник"
        verbose_name_plural = "Источники лидов"
        ordering = ["sort_order", "pk"]

    def __str__(self):
        return self.name


class CrmTag(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name="Тег")
    color = models.CharField(max_length=7, default="#78716c", verbose_name="Цвет")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ["name"]

    def __str__(self):
        return self.name


class CrmContact(models.Model):
    name = models.CharField(max_length=200, verbose_name="Имя")
    phone = models.CharField(max_length=32, db_index=True, verbose_name="Телефон")
    email = models.EmailField(blank=True, verbose_name="Email")
    company_name = models.CharField(max_length=200, blank=True, verbose_name="Компания")
    notes = models.TextField(blank=True, verbose_name="Заметки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлён")

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
        ordering = ["-updated_at"]

    def __str__(self):
        return self.name or self.phone


class CrmDeal(models.Model):
    PRIORITY_LOW = "low"
    PRIORITY_NORMAL = "normal"
    PRIORITY_HIGH = "high"
    PRIORITY_CHOICES = [
        (PRIORITY_LOW, "Низкий"),
        (PRIORITY_NORMAL, "Обычный"),
        (PRIORITY_HIGH, "Высокий"),
    ]

    title = models.CharField(max_length=255, verbose_name="Название сделки")
    contact = models.ForeignKey(
        CrmContact,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="deals",
        verbose_name="Контакт",
    )
    pipeline = models.ForeignKey(
        CrmPipeline,
        on_delete=models.PROTECT,
        related_name="deals",
        verbose_name="Воронка",
    )
    stage = models.ForeignKey(
        CrmStage,
        on_delete=models.PROTECT,
        related_name="deals",
        verbose_name="Этап",
    )
    responsible = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="crm_deals",
        verbose_name="Ответственный",
    )
    source = models.ForeignKey(
        CrmLeadSource,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="deals",
        verbose_name="Источник",
    )
    tags = models.ManyToManyField(CrmTag, blank=True, related_name="deals", verbose_name="Теги")
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Бюджет, ₽",
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    priority = models.CharField(
        max_length=8,
        choices=PRIORITY_CHOICES,
        default=PRIORITY_NORMAL,
        verbose_name="Приоритет",
    )
    lost_reason = models.CharField(max_length=255, blank=True, verbose_name="Причина отказа")
    site_lead = models.OneToOneField(
        "main.ContactLead",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="crm_deal",
        verbose_name="Заявка с сайта",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлена")
    closed_at = models.DateTimeField(null=True, blank=True, verbose_name="Закрыта")

    class Meta:
        verbose_name = "Сделка"
        verbose_name_plural = "Сделки"
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title

    @property
    def is_closed(self):
        return self.stage.stage_type in (CrmStage.TYPE_WON, CrmStage.TYPE_LOST)

    def move_to_stage(self, stage, *, user=None, note=""):
        if stage.pipeline_id != self.pipeline_id:
            raise ValueError("Этап должен принадлежать воронке сделки")
        self._stage_change_user = user
        self._stage_change_note = note
        self.stage = stage
        self.save()


class CrmTask(models.Model):
    deal = models.ForeignKey(
        CrmDeal,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="Сделка",
    )
    title = models.CharField(max_length=255, verbose_name="Задача")
    due_at = models.DateTimeField(null=True, blank=True, verbose_name="Срок")
    is_done = models.BooleanField(default=False, verbose_name="Выполнена")
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="crm_tasks",
        verbose_name="Исполнитель",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Завершена")

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ["is_done", "due_at", "-created_at"]

    def __str__(self):
        return self.title

    def mark_done(self):
        self.is_done = True
        self.completed_at = timezone.now()
        self.save(update_fields=["is_done", "completed_at"])


class CrmActivity(models.Model):
    TYPE_NOTE = "note"
    TYPE_CALL = "call"
    TYPE_MEETING = "meeting"
    TYPE_EMAIL = "email"
    TYPE_STAGE = "stage_change"
    TYPE_CREATED = "created"
    TYPE_CHOICES = [
        (TYPE_NOTE, "Заметка"),
        (TYPE_CALL, "Звонок"),
        (TYPE_MEETING, "Встреча"),
        (TYPE_EMAIL, "Письмо"),
        (TYPE_STAGE, "Смена этапа"),
        (TYPE_CREATED, "Создание"),
    ]

    deal = models.ForeignKey(
        CrmDeal,
        on_delete=models.CASCADE,
        related_name="activities",
        verbose_name="Сделка",
    )
    activity_type = models.CharField(
        max_length=16,
        choices=TYPE_CHOICES,
        default=TYPE_NOTE,
        verbose_name="Тип",
    )
    body = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="crm_activities",
        verbose_name="Автор",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    class Meta:
        verbose_name = "Активность"
        verbose_name_plural = "Активности"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_activity_type_display()} — {self.deal_id}"
