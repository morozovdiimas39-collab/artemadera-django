from django.db import models


class CalculatorConfig(models.Model):
    """Единственная запись — общие настройки слайдера площади."""

    area_min = models.PositiveIntegerField(default=20, verbose_name="Мин. площадь, м²")
    area_max = models.PositiveIntegerField(default=300, verbose_name="Макс. площадь, м²")
    area_step = models.PositiveIntegerField(default=5, verbose_name="Шаг, м²")
    area_default = models.PositiveIntegerField(default=75, verbose_name="Площадь по умолчанию, м²")

    class Meta:
        verbose_name = "Настройки калькулятора"
        verbose_name_plural = "Настройки калькулятора"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Настройки калькулятора"


class HomeQuizSettings(models.Model):
    """Единственная запись — картинка справа в квизе на главной (по выбору услуги)."""

    default_image = models.ImageField(
        upload_to="home_quiz/",
        blank=True,
        null=True,
        verbose_name="Фото по умолчанию (до выбора)",
    )
    image_shlifovka = models.ImageField(
        upload_to="home_quiz/",
        blank=True,
        null=True,
        verbose_name="Шлифовка",
    )
    image_pokraska = models.ImageField(
        upload_to="home_quiz/",
        blank=True,
        null=True,
        verbose_name="Покраска",
    )
    image_teplyy_shov = models.ImageField(
        upload_to="home_quiz/",
        blank=True,
        null=True,
        verbose_name="Тёплый шов",
    )
    image_okosyachka = models.ImageField(
        upload_to="home_quiz/",
        blank=True,
        null=True,
        verbose_name="Окосячка",
    )
    image_obsada = models.ImageField(
        upload_to="home_quiz/",
        blank=True,
        null=True,
        verbose_name="Обсада",
    )
    image_kryshi = models.ImageField(
        upload_to="home_quiz/",
        blank=True,
        null=True,
        verbose_name="Крыши",
    )
    image_injeneriya = models.ImageField(
        upload_to="home_quiz/",
        blank=True,
        null=True,
        verbose_name="Инженерия",
    )

    class Meta:
        verbose_name = "Квиз на главной — картинки"
        verbose_name_plural = "Квиз на главной — картинки"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Квиз на главной — картинки"


class CalculatorMaterial(models.Model):
    key = models.SlugField(
        max_length=32,
        unique=True,
        verbose_name="Код (srub, brus, kleen, banya)",
    )
    label = models.CharField(max_length=120, verbose_name="Название в калькуляторе")
    price_per_sqm = models.PositiveIntegerField(verbose_name="Цена за м², ₽")
    sort_order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Показывать")

    class Meta:
        verbose_name = "Материал калькулятора"
        verbose_name_plural = "Материалы калькулятора"
        ordering = ["sort_order", "pk"]

    def __str__(self):
        return f"{self.label} — {self.price_per_sqm} ₽/м²"


class CalculatorProfile(models.Model):
  UNIT_SQM = "sqm"
  UNIT_LINEAR = "linear"
  UNIT_FIXED = "fixed"
  UNIT_CHOICES = [
    (UNIT_SQM, "Площадь (м²)"),
    (UNIT_LINEAR, "Длина (м.п.)"),
    (UNIT_FIXED, "Фиксированные пакеты"),
  ]

  slug = models.SlugField(
    max_length=48,
    unique=True,
    verbose_name="Код страницы (home, shlifovka, pokraska…)",
  )
  name = models.CharField(max_length=120, verbose_name="Название в админке")
  badge_text = models.CharField(max_length=64, default="КАЛЬКУЛЯТОР", verbose_name="Бейдж")
  title = models.CharField(max_length=120, default="Онлайн-калькулятор", verbose_name="Заголовок")
  description = models.TextField(
    default="Узнайте примерную стоимость. Точную смету рассчитаем после осмотра.",
    verbose_name="Описание",
  )
  perk_1 = models.CharField(
    max_length=200,
    default="Бесплатный расчёт — под ваш объект",
    verbose_name="Преимущество 1",
  )
  perk_2 = models.CharField(
    max_length=200,
    default="Перезвон за 30 минут",
    verbose_name="Преимущество 2",
  )
  perk_3 = models.CharField(
    max_length=200,
    default="Консультация по срокам и этапам",
    verbose_name="Преимущество 3",
  )
  options_label = models.CharField(
    max_length=120,
    default="Материал дома",
    verbose_name="Подпись блока вариантов",
  )
  unit_type = models.CharField(
    max_length=16,
    choices=UNIT_CHOICES,
    default=UNIT_SQM,
    verbose_name="Тип расчёта",
  )
  unit_label = models.CharField(max_length=32, default="м²", verbose_name="Единица измерения")
  area_min = models.PositiveIntegerField(default=20, verbose_name="Мин. значение слайдера")
  area_max = models.PositiveIntegerField(default=300, verbose_name="Макс. значение слайдера")
  area_step = models.PositiveIntegerField(default=5, verbose_name="Шаг слайдера")
  area_default = models.PositiveIntegerField(default=75, verbose_name="Значение по умолчанию")
  show_service_picker = models.BooleanField(
    default=False,
    verbose_name="Квиз выбора услуги (для главной)",
  )
  submit_button_text = models.CharField(
    max_length=64,
    default="Зафиксировать цену",
    verbose_name="Текст кнопки отправки",
  )
  is_active = models.BooleanField(default=True, verbose_name="Активен")
  sort_order = models.IntegerField(default=0, verbose_name="Порядок")

  class Meta:
    verbose_name = "Калькулятор (страница)"
    verbose_name_plural = "Калькуляторы по страницам"
    ordering = ["sort_order", "pk"]

  def min_active_price(self):
    agg = self.options.filter(is_active=True).aggregate(m=models.Min("price_per_unit"))
    return agg["m"]

  def home_price_tag(self):
    """Бейдж «от …» для карточки на главной — из минимальной цены вариантов."""
    price = self.min_active_price()
    if price is None:
      return ""
    formatted = f"{price:,}".replace(",", "\u00a0")
    if self.unit_type == self.UNIT_SQM:
      return f"от {formatted} ₽/{self.unit_label}"
    if self.unit_type == self.UNIT_LINEAR:
      return f"от {formatted} ₽/{self.unit_label}"
    return f"от {formatted} ₽"

  def __str__(self):
    return self.name


class CalculatorOption(models.Model):
  profile = models.ForeignKey(
    CalculatorProfile,
    on_delete=models.CASCADE,
    related_name="options",
    verbose_name="Калькулятор",
  )
  key = models.SlugField(max_length=48, verbose_name="Код варианта")
  label = models.CharField(max_length=120, verbose_name="Название")
  price_per_unit = models.PositiveIntegerField(verbose_name="Цена за единицу, ₽")
  sort_order = models.IntegerField(default=0, verbose_name="Порядок")
  is_active = models.BooleanField(default=True, verbose_name="Показывать")

  class Meta:
    verbose_name = "Вариант калькулятора"
    verbose_name_plural = "Варианты калькулятора"
    ordering = ["sort_order", "pk"]
    unique_together = [["profile", "key"]]

  def __str__(self):
    return f"{self.profile.slug}: {self.label}"


class CalculatorServiceChoice(models.Model):
  """Пункты квиза на главной — выбор направления услуги."""

  profile = models.ForeignKey(
    CalculatorProfile,
    on_delete=models.CASCADE,
    related_name="service_choices",
    verbose_name="Калькулятор (главная)",
  )
  label = models.CharField(max_length=120, verbose_name="Название услуги")
  target_profile = models.ForeignKey(
    CalculatorProfile,
    on_delete=models.CASCADE,
    related_name="linked_from_choices",
    verbose_name="Калькулятор услуги",
  )
  hint = models.CharField(max_length=160, blank=True, verbose_name="Подпись")
  sort_order = models.IntegerField(default=0, verbose_name="Порядок")
  is_active = models.BooleanField(default=True, verbose_name="Показывать")

  class Meta:
    verbose_name = "Услуга в квизе"
    verbose_name_plural = "Услуги в квизе"
    ordering = ["sort_order", "pk"]

  def __str__(self):
    return self.label


class Service(models.Model):
    LAYOUT_DEFAULT = ""
    LAYOUT_WIDE = "wide"
    LAYOUT_LAST = "last"
    LAYOUT_HALF = "half"
    LAYOUT_CHOICES = [
        (LAYOUT_DEFAULT, "Обычная"),
        (LAYOUT_WIDE, "Широкая (2 колонки)"),
        (LAYOUT_LAST, "Широкая в конце сетки"),
        (LAYOUT_HALF, "Половина ряда (6/12)"),
    ]

    name = models.CharField(max_length=200, verbose_name="Название услуги")
    slug = models.SlugField(unique=True, verbose_name="Слаг (URL)")
    short_description = models.TextField(verbose_name="Краткое описание", blank=True)
    description = models.TextField(verbose_name="Полное описание", blank=True)
    price_from = models.IntegerField(
        verbose_name="Цена от (ручная, если нет калькулятора)",
        null=True,
        blank=True,
        help_text="Используется только если не выбран калькулятор и нет бейджа вручную.",
    )
    calculator_profile = models.ForeignKey(
        CalculatorProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="homepage_services",
        verbose_name="Калькулятор",
        help_text="Минимальная цена из вариантов калькулятора — в бейдж на главной.",
    )
    image = models.ImageField(
        upload_to="services/",
        verbose_name="Фото на главной",
        null=True,
        blank=True,
    )
    static_image = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Фото (static)",
        help_text="Например images/quiz/quiz_shlifovka_1776809850085.png — если нет загрузки.",
    )
    home_tag_override = models.CharField(
        max_length=64,
        blank=True,
        verbose_name="Бейдж на главной (вручную)",
        help_text="Напр. «под ключ». Пусто — цена из калькулятора.",
    )
    page_url = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Ссылка",
        help_text="Напр. /obsada/okna. Пусто — /slug/",
    )
    home_layout = models.CharField(
        max_length=16,
        choices=LAYOUT_CHOICES,
        default=LAYOUT_DEFAULT,
        blank=True,
        verbose_name="Раскладка на главной",
        help_text="Для страницы «Шлифовка» также задаёт ширину карточки в сетке блока услуг.",
    )
    show_on_homepage = models.BooleanField(
        default=False,
        verbose_name="Показывать на главной",
    )
    icon = models.CharField(max_length=50, verbose_name="Иконка (Lucide name)", blank=True)
    order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ["order", "name"]

    @property
    def has_image(self):
        return bool(self.image) or bool(self.static_image)

    @property
    def link_url(self):
        if self.page_url.strip():
            url = self.page_url.strip()
            return url if url.startswith("/") else f"/{url}"
        return f"/{self.slug}/"

    def get_home_tag(self):
        if self.home_tag_override.strip():
            return self.home_tag_override.strip()
        if self.calculator_profile_id:
            tag = self.calculator_profile.home_price_tag()
            if tag:
                return tag
        if self.price_from:
            formatted = f"{self.price_from:,}".replace(",", "\u00a0")
            return f"от {formatted} ₽"
        return ""

    def __str__(self):
        return self.name


class SitePage(models.Model):
    """Единая настройка страницы: hero, блок услуг, привязка к URL."""

    page_key = models.CharField(
        max_length=160,
        unique=True,
        verbose_name="URL страницы",
        help_text="Без начального слэша: home — главная, obsada/okna — /obsada/okna",
    )
    title = models.CharField(max_length=120, verbose_name="Название в админке")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    sort_order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")

    hero_image = models.ImageField(
        upload_to="pages/hero/",
        blank=True,
        null=True,
        verbose_name="Загрузить фон",
        help_text="Кнопка загрузки справа — выберите файл, затем «Сохранить» внизу формы.",
    )
    hero_static_image = models.CharField(
        max_length=200,
        blank=True,
        default="images/hero-bg.jpg",
        verbose_name="Запасной фон (файл в static)",
        help_text="Используется только если выше не загружено изображение.",
    )
    hero_h1_white = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Заголовок H1 (белая часть)",
    )
    hero_h1_accent = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Заголовок H1 (акцент)",
        help_text="Можно перенос строки — отобразится как <br>",
    )
    hero_lead = models.TextField(blank=True, verbose_name="Подзаголовок под H1")

    show_services_block = models.BooleanField(
        default=False,
        verbose_name="Показывать блок услуг",
    )
    services_badge = models.CharField(
        max_length=64,
        blank=True,
        default="",
        verbose_name="Бейдж блока услуг",
        help_text="Пусто — в блоке на странице подставится короткая подпись из названия страницы.",
    )
    services_title_white = models.CharField(
        max_length=120,
        blank=True,
        verbose_name="Заголовок услуг (белый)",
    )
    services_title_accent = models.CharField(
        max_length=120,
        blank=True,
        verbose_name="Заголовок услуг (акцент)",
    )
    services_lead = models.TextField(blank=True, verbose_name="Текст под заголовком услуг")

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"
        ordering = ("sort_order", "title")

    @property
    def url_path(self):
        return "/" if self.page_key == "home" else f"/{self.page_key}"

    @property
    def has_hero_upload(self):
        return bool(self.hero_image and self.hero_image.name)

    def __str__(self):
        return self.title or self.page_key


class PageServiceLink(models.Model):
    """Услуга на конкретной странице (из общего справочника)."""

    LAYOUT_DEFAULT = ""
    LAYOUT_WIDE = "wide"
    LAYOUT_LAST = "last"
    LAYOUT_HALF = "half"
    LAYOUT_CHOICES = [
        (LAYOUT_DEFAULT, "Обычная"),
        (LAYOUT_WIDE, "Широкая (2 колонки)"),
        (LAYOUT_LAST, "Широкая в конце сетки"),
        (LAYOUT_HALF, "Половина ряда (6/12)"),
    ]

    page = models.ForeignKey(
        SitePage,
        on_delete=models.CASCADE,
        related_name="service_links",
        verbose_name="Страница",
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="page_links",
        verbose_name="Услуга",
    )
    sort_order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")
    layout = models.CharField(
        max_length=16,
        choices=LAYOUT_CHOICES,
        default=LAYOUT_DEFAULT,
        blank=True,
        verbose_name="Раскладка карточки",
    )
    tag_override = models.CharField(
        max_length=64,
        blank=True,
        verbose_name="Бейдж (вручную)",
        help_text="Пусто — из калькулятора услуги.",
    )
    cta_label = models.CharField(
        max_length=80,
        blank=True,
        default="",
        verbose_name="Текст кнопки на карточке",
        help_text="Пусто — «Узнать подробнее».",
    )
    is_visible = models.BooleanField(default=True, verbose_name="Показывать")

    class Meta:
        verbose_name = "Услуга на странице"
        verbose_name_plural = "Услуги на странице"
        ordering = ("sort_order", "pk")
        unique_together = [["page", "service"]]

    def get_tag(self):
        if self.tag_override.strip():
            return self.tag_override.strip()
        return self.service.get_home_tag()

    def __str__(self):
        return f"{self.page}: {self.service.name}"


class PortfolioSection(models.Model):
    """Тексты блока «Наши проекты» (одна запись)."""

    badge_text = models.CharField(max_length=64, default="ПОРТФОЛИО", verbose_name="Бейдж")
    title_prefix = models.CharField(max_length=64, default="Наши", verbose_name="Заголовок (белая часть)")
    title_highlight = models.CharField(
        max_length=64, default="проекты", verbose_name="Заголовок (акцент)"
    )
    description = models.TextField(
        default=(
            "Оцените качество нашей работы: мы бережно восстанавливаем древесину, "
            "возвращая домам первозданный вид и надёжную защиту."
        ),
        verbose_name="Описание",
    )
    is_visible = models.BooleanField(default=True, verbose_name="Показывать блок")

    class Meta:
        verbose_name = "Блок «Наши проекты»"
        verbose_name_plural = "Блок «Наши проекты»"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Наши проекты"


class PortfolioProject(models.Model):
    HOUSE_SRUB = "srub"
    HOUSE_BRUS = "brus"
    HOUSE_OCIL = "ocil"
    HOUSE_BANYA = "banya"
    HOUSE_KLEEN = "kleen"
    HOUSE_OTHER = "other"
    HOUSE_TYPE_CHOICES = [
        (HOUSE_SRUB, "Сруб"),
        (HOUSE_BRUS, "Брус"),
        (HOUSE_OCIL, "Оцилиндровка"),
        (HOUSE_BANYA, "Баня / сауна"),
        (HOUSE_KLEEN, "Клеёный брус"),
        (HOUSE_OTHER, "Другое"),
    ]

    title = models.CharField(
        max_length=200,
        blank=True,
        default="",
        verbose_name="Название (необязательно)",
        help_text="Можно оставить пустым: на сайте будет показано только фото.",
    )
    summary = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="Кратко (на карточке)",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание (в раскрытии)",
    )
    house_type = models.CharField(
        max_length=16,
        choices=HOUSE_TYPE_CHOICES,
        blank=True,
        verbose_name="Тип дома",
    )
    location = models.CharField(max_length=200, blank=True, verbose_name="Локация")
    work_types = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Услуги",
        help_text="Через запятую: шлифовка, покраска",
    )
    has_before_after = models.BooleanField(
        default=False,
        verbose_name="Есть серия «До/После»",
    )
    image = models.ImageField(
        upload_to="portfolio/",
        blank=True,
        null=True,
        verbose_name="Обложка (устарело)",
        help_text="Не используется — загружайте фото в галерею ниже.",
    )
    static_image = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Обложка static (устарело)",
    )
    alt_text = models.CharField(max_length=255, blank=True, verbose_name="Alt (устарело)")
    sort_order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Показывать")

    class Meta:
        verbose_name = "Кейс"
        verbose_name_plural = "Кейсы"
        ordering = ["sort_order", "pk"]

    def __str__(self):
        return self.display_title

    @property
    def display_title(self):
        title = (self.title or "").strip()
        if title:
            return title
        cover = self.cover_item()
        if cover and getattr(cover, "caption", ""):
            return cover.caption.strip()
        return f"Работа #{self.pk or ''}".strip()

    @property
    def has_text_content(self):
        return any(
            [
                (self.title or "").strip(),
                (self.summary or "").strip(),
                (self.description or "").strip(),
                (self.location or "").strip(),
                (self.house_type or "").strip(),
                (self.work_types or "").strip(),
                self.has_before_after,
            ]
        )

    @property
    def house_type_label(self):
        if not self.house_type:
            return ""
        return dict(self.HOUSE_TYPE_CHOICES).get(self.house_type, "")

    @property
    def work_types_list(self):
        if not self.work_types:
            return []
        return [t.strip() for t in self.work_types.split(",") if t.strip()]

    @property
    def has_legacy_cover(self):
        return bool(self.image) or bool(self.static_image)

    def get_gallery_items(self):
        if hasattr(self, "_prefetched_objects_cache") and "photos" in self._prefetched_objects_cache:
            photos = [
                photo
                for photo in self._prefetched_objects_cache["photos"]
                if photo.is_active
            ]
            photos.sort(key=lambda photo: (photo.sort_order, photo.pk or 0))
        else:
            photos = list(self.photos.filter(is_active=True).order_by("sort_order", "pk"))
        if photos:
            return photos
        if self.has_legacy_cover:
            return [self]
        return []

    @property
    def has_image(self):
        return bool(self.get_gallery_items())

    def cover_item(self):
        items = self.get_gallery_items()
        return items[0] if items else None

    def is_photo_model(self, item):
        return item.__class__.__name__ == "PortfolioProjectImage"


class PortfolioProjectImage(models.Model):
    project = models.ForeignKey(
        PortfolioProject,
        on_delete=models.CASCADE,
        related_name="photos",
        verbose_name="Кейс",
    )
    image = models.ImageField(
        upload_to="portfolio/cases/",
        blank=True,
        null=True,
        verbose_name="Фото",
    )
    static_image = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Static (запас)",
        help_text="Только для старых записей: images/portfolio-1.jpg",
    )
    caption = models.CharField(max_length=200, blank=True, verbose_name="Подпись")
    is_cover = models.BooleanField(
        default=False,
        verbose_name="Обложка (служебное)",
        editable=False,
    )
    sort_order = models.IntegerField(
        default=0,
        verbose_name="№",
        help_text="0 — обложка на карточке, дальше 1, 2, 3…",
    )
    is_active = models.BooleanField(default=True, verbose_name="Показывать")

    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Фото"
        ordering = ["sort_order", "pk"]

    def __str__(self):
        return self.caption or f"Фото #{self.pk}"

    @property
    def has_file(self):
        return bool(self.image) or bool(self.static_image)


class ExperienceSection(models.Model):
    """Блок «Опыт компании» (одна запись)."""

    badge_text = models.CharField(
        max_length=64, default="ОПЫТ И НАДЁЖНОСТЬ", verbose_name="Бейдж"
    )
    title_prefix = models.CharField(
        max_length=80, default="Более", verbose_name="Заголовок (белая часть)"
    )
    title_highlight = models.CharField(
        max_length=80,
        default="10 лет с деревом",
        verbose_name="Заголовок (акцент)",
    )
    description = models.TextField(
        default=(
            "Строительно-отделочная компания полного цикла для деревянных домов "
            "в Москве и области — от шлифовки и покраски до кровли и инженерии."
        ),
        verbose_name="Краткое описание",
    )
    story = models.TextField(
        default=(
            "ArteMadera объединяет комплекс отделочных работ у одного исполнителя: "
            "не нужно искать разных подрядчиков и согласовывать сроки. Работаем по договору "
            "с фиксированной сметой, используем сертифицированные материалы и собственное "
            "производство. На замере можем бесплатно показать качество — «тест-драйв» "
            "на участке вашего дома."
        ),
        verbose_name="Текст о компании",
    )
    image = models.ImageField(
        upload_to="experience/",
        blank=True,
        null=True,
        verbose_name="Фото (загрузка)",
    )
    static_image = models.CharField(
        max_length=200,
        default="images/team.png",
        blank=True,
        verbose_name="Фото из static",
    )
    is_visible = models.BooleanField(default=True, verbose_name="Показывать блок")

    class Meta:
        verbose_name = "Блок «Опыт компании»"
        verbose_name_plural = "Блок «Опыт компании»"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Опыт компании"


class ExperienceStat(models.Model):
    value = models.CharField(max_length=32, verbose_name="Значение")
    label = models.CharField(max_length=120, verbose_name="Подпись")
    sort_order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Показывать")

    class Meta:
        verbose_name = "Показатель опыта"
        verbose_name_plural = "Показатели опыта"
        ordering = ["sort_order", "pk"]

    def __str__(self):
        return f"{self.value} — {self.label}"


class ExperienceAdvantage(models.Model):
    ICON_CONTRACT = "contract"
    ICON_WALLET = "wallet"
    ICON_SHIELD = "shield"
    ICON_SPARKLES = "sparkles"
    ICON_FACTORY = "factory"
    ICON_CERTIFICATE = "certificate"
    ICON_CHOICES = [
        (ICON_CONTRACT, "Договор"),
        (ICON_WALLET, "Смета"),
        (ICON_SHIELD, "Гарантия"),
        (ICON_SPARKLES, "Тест-драйв"),
        (ICON_FACTORY, "Производство"),
        (ICON_CERTIFICATE, "Сертификаты"),
    ]

    title = models.CharField(max_length=120, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    icon = models.CharField(
        max_length=32,
        choices=ICON_CHOICES,
        default=ICON_CONTRACT,
        verbose_name="Иконка",
    )
    sort_order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Показывать")

    class Meta:
        verbose_name = "Преимущество"
        verbose_name_plural = "Преимущества (опыт)"
        ordering = ["sort_order", "pk"]

    def __str__(self):
        return self.title


class ReviewsSection(models.Model):
    badge_text = models.CharField(max_length=64, default="ОТЗЫВЫ", verbose_name="Бейдж")
    title_prefix = models.CharField(max_length=64, default="Что говорят", verbose_name="Заголовок (белая часть)")
    title_highlight = models.CharField(
        max_length=64, default="клиенты", verbose_name="Заголовок (акцент)"
    )
    description = models.TextField(
        default=(
            "Реальные отзывы с Яндекс.Карт и сайта ArteMadera — о шлифовке, "
            "отделке и работе команды на объекте."
        ),
        verbose_name="Описание",
    )
    yandex_maps_url = models.URLField(
        default="https://yandex.ru/maps/org/artemadera/45828270851/",
        verbose_name="Ссылка на Яндекс.Карты",
    )
    yandex_rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=4.8,
        verbose_name="Рейтинг (для отображения)",
    )
    yandex_reviews_count = models.PositiveIntegerField(
        default=0,
        blank=True,
        verbose_name="Кол-во отзывов (0 — не показывать)",
    )
    is_visible = models.BooleanField(default=True, verbose_name="Показывать блок")

    class Meta:
        verbose_name = "Блок «Отзывы»"
        verbose_name_plural = "Блок «Отзывы»"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Отзывы"


class Review(models.Model):
    SOURCE_YANDEX = "yandex"
    SOURCE_SITE = "site"
    SOURCE_CHOICES = [
        (SOURCE_YANDEX, "Яндекс.Карты"),
        (SOURCE_SITE, "Сайт"),
    ]

    author_name = models.CharField(max_length=120, verbose_name="Имя автора")
    headline = models.CharField(max_length=200, verbose_name="Заголовок отзыва")
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.PositiveSmallIntegerField(default=5, verbose_name="Оценка (1–5)")
    source = models.CharField(
        max_length=16,
        choices=SOURCE_CHOICES,
        default=SOURCE_YANDEX,
        verbose_name="Источник",
    )
    sort_order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Показывать")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["sort_order", "pk"]

    def __str__(self):
        return f"{self.author_name} — {self.headline}"


class WorkProcessSection(models.Model):
    badge_text = models.CharField(max_length=64, default="КАК МЫ РАБОТАЕМ", verbose_name="Бейдж")
    title_prefix = models.CharField(max_length=80, default="Этапы", verbose_name="Заголовок (белая часть)")
    title_highlight = models.CharField(
        max_length=80, default="нашей работы", verbose_name="Заголовок (акцент)"
    )
    description = models.TextField(
        default=(
            "Прозрачный и отлаженный процесс — от первого звонка "
            "до сдачи готового объекта."
        ),
        verbose_name="Описание",
    )
    is_visible = models.BooleanField(default=True, verbose_name="Показывать блок")

    class Meta:
        verbose_name = "Блок «Этапы работы»"
        verbose_name_plural = "Блок «Этапы работы»"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Этапы работы"


class WorkProcessStep(models.Model):
    step_number = models.CharField(max_length=4, verbose_name="Номер (01, 02…)")
    title = models.CharField(max_length=120, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    sort_order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Показывать")

    class Meta:
        verbose_name = "Этап работы"
        verbose_name_plural = "Этапы работы"
        ordering = ["sort_order", "pk"]

    def __str__(self):
        return f"{self.step_number} — {self.title}"


class ContactSection(models.Model):
    badge_text = models.CharField(max_length=64, default="СВЯЗАТЬСЯ", verbose_name="Бейдж")
    title_prefix = models.CharField(max_length=80, default="Оставьте", verbose_name="Заголовок (белая часть)")
    title_highlight = models.CharField(
        max_length=80, default="заявку", verbose_name="Заголовок (акцент)"
    )
    description = models.TextField(
        default=(
            "Расскажите о вашем доме — перезвоним в течение 30 минут, "
            "ответим на вопросы и согласуем выезд на замер."
        ),
        verbose_name="Описание",
    )
    phone = models.CharField(max_length=32, default="+7 (495) 005-01-45", verbose_name="Телефон")
    phone_href = models.CharField(
        max_length=20, default="74950050145", verbose_name="Телефон (цифры для ссылки)"
    )
    email = models.EmailField(default="info@artemadera.ru", verbose_name="Email")
    work_hours = models.CharField(
        max_length=120, default="Пн–Пт, 9:00–21:00", verbose_name="Часы работы"
    )
    address = models.CharField(
        max_length=255,
        default="г. Москва, м. ВДНХ, Ярославская ул., д. 8, корп. 6, офис 220",
        blank=True,
        verbose_name="Адрес",
    )
    submit_button_text = models.CharField(
        max_length=64, default="Отправить заявку", verbose_name="Текст кнопки"
    )
    privacy_note = models.CharField(
        max_length=255,
        default="Нажимая кнопку, вы соглашаетесь с обработкой персональных данных",
        verbose_name="Примечание под формой",
    )
    is_visible = models.BooleanField(default=True, verbose_name="Показывать блок")

    class Meta:
        verbose_name = "Блок «Обратная связь»"
        verbose_name_plural = "Блок «Обратная связь»"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Обратная связь"


class LeadEmailSettings(models.Model):
    """Куда отправлять письмо при каждой новой заявке с форм сайта (ContactLead)."""

    notification_emails = models.TextField(
        blank=True,
        verbose_name="Email для уведомлений",
        help_text=(
            "Один или несколько адресов — через запятую или с новой строки. "
            "Пока поле пустое, письма не отправляются."
        ),
    )
    smtp_login = models.EmailField(
        blank=True,
        verbose_name="Логин SMTP",
        help_text="Корпоративная почта, от имени которой отправляются уведомления. Если пусто — берётся EMAIL_HOST_USER из окружения.",
    )
    smtp_password = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Пароль приложения SMTP",
        help_text="Пароль приложения из Яндекс ID. Хранится в базе как обычная строка.",
    )
    smtp_host = models.CharField(
        max_length=120,
        blank=True,
        default="smtp.yandex.ru",
        verbose_name="SMTP host",
    )
    smtp_port = models.PositiveIntegerField(default=587, verbose_name="SMTP port")
    smtp_use_tls = models.BooleanField(default=True, verbose_name="TLS")
    smtp_use_ssl = models.BooleanField(default=False, verbose_name="SSL")

    class Meta:
        verbose_name = "Уведомления о заявках (email)"
        verbose_name_plural = "Уведомления о заявках (email)"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Куда слать заявки"


class ContactLead(models.Model):
    DIRECT_STATUS_IN_PROGRESS = "IN_PROGRESS"
    DIRECT_STATUS_PAID = "PAID"
    DIRECT_STATUS_CANCELLED = "CANCELLED"
    DIRECT_STATUS_SPAM = "SPAM"
    DIRECT_STATUS_CHOICES = [
        (DIRECT_STATUS_IN_PROGRESS, "Целевой"),
        (DIRECT_STATUS_PAID, "Оплачен"),
        (DIRECT_STATUS_CANCELLED, "Нецелевой"),
        (DIRECT_STATUS_SPAM, "Спам"),
    ]

    name = models.CharField(max_length=120, verbose_name="Имя")
    phone = models.CharField(max_length=32, verbose_name="Телефон")
    message = models.TextField(blank=True, verbose_name="Сообщение")
    ym_client_id = models.CharField(
        max_length=32,
        blank=True,
        verbose_name="ClientID Метрики (_ym_uid)",
        help_text="Числовой идентификатор для офлайн-конверсий в Директе; можно передавать из формы скрытым полем.",
    )
    page_url = models.URLField(max_length=500, blank=True, verbose_name="Страница заявки")
    landing_page = models.URLField(max_length=500, blank=True, verbose_name="Посадочная страница")
    referrer = models.URLField(max_length=500, blank=True, verbose_name="Referrer")
    utm_source = models.CharField(max_length=255, blank=True, verbose_name="UTM source")
    utm_medium = models.CharField(max_length=255, blank=True, verbose_name="UTM medium")
    utm_campaign = models.CharField(max_length=255, blank=True, verbose_name="UTM campaign")
    utm_content = models.CharField(max_length=255, blank=True, verbose_name="UTM content")
    utm_term = models.CharField(max_length=255, blank=True, verbose_name="UTM term")
    yclid = models.CharField(max_length=255, blank=True, verbose_name="Yandex Click ID")
    gclid = models.CharField(max_length=255, blank=True, verbose_name="Google Click ID")
    fbclid = models.CharField(max_length=255, blank=True, verbose_name="Facebook Click ID")
    ymclid = models.CharField(max_length=255, blank=True, verbose_name="Yandex Metrika Click ID")
    direct_status = models.CharField(
        max_length=16,
        choices=DIRECT_STATUS_CHOICES,
        default=DIRECT_STATUS_IN_PROGRESS,
        verbose_name="Статус для CSV Директа",
        help_text="Меняется из письма кнопками: целевой, нецелевой, спам, оплачен.",
    )
    direct_status_updated_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Статус CSV обновлён",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    class Meta:
        verbose_name = "Заявка с сайта"
        verbose_name_plural = "Заявки с сайта"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.phone}"

    def traffic_summary(self):
        if self.utm_source:
            return self.utm_source
        if self.yclid:
            return "Яндекс"
        if self.gclid:
            return "Google"
        if self.fbclid:
            return "Facebook"
        if self.referrer:
            return self.referrer[:80]
        return "—"


class FaqSection(models.Model):
    badge_text = models.CharField(max_length=64, default="ВОПРОСЫ", verbose_name="Бейдж")
    title_prefix = models.CharField(max_length=80, default="Частые", verbose_name="Заголовок (белая часть)")
    title_highlight = models.CharField(
        max_length=80, default="вопросы", verbose_name="Заголовок (акцент)"
    )
    description = models.TextField(
        default="Ответы на популярные вопросы о шлифовке деревянных домов.",
        verbose_name="Описание",
    )
    is_visible = models.BooleanField(default=True, verbose_name="Показывать блок")

    class Meta:
        verbose_name = "Блок «FAQ»"
        verbose_name_plural = "Блок «FAQ»"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "FAQ"


class FaqItem(models.Model):
    question = models.CharField(max_length=300, verbose_name="Вопрос")
    answer = models.TextField(verbose_name="Ответ")
    sort_order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Показывать")

    class Meta:
        verbose_name = "Вопрос FAQ"
        verbose_name_plural = "Вопросы FAQ"
        ordering = ["sort_order", "pk"]

    def __str__(self):
        return self.question[:80]


class BeforeAfterSection(models.Model):
    badge_text = models.CharField(max_length=64, default="РЕЗУЛЬТАТ", verbose_name="Бейдж")
    title_prefix = models.CharField(max_length=80, default="До и", verbose_name="Заголовок (белая часть)")
    title_highlight = models.CharField(
        max_length=80, default="после", verbose_name="Заголовок (акцент)"
    )
    description = models.TextField(
        default="Сравните состояние древесины до и после профессиональной шлифовки.",
        verbose_name="Описание",
    )
    is_visible = models.BooleanField(default=True, verbose_name="Показывать блок")

    class Meta:
        verbose_name = "Блок «До / После»"
        verbose_name_plural = "Блок «До / После»"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "До / После"


class BeforeAfterItem(models.Model):
    page = models.ForeignKey(
        SitePage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="before_after_items",
        verbose_name="Страница услуги",
        help_text="Пусто — показывать как общий пример на всех страницах.",
    )
    title = models.CharField(max_length=200, verbose_name="Подпись")
    before_image = models.ImageField(
        upload_to="before_after/", blank=True, null=True, verbose_name="Фото «До»"
    )
    after_image = models.ImageField(
        upload_to="before_after/", blank=True, null=True, verbose_name="Фото «После»"
    )
    before_static = models.CharField(max_length=200, blank=True, verbose_name="До (static)")
    after_static = models.CharField(max_length=200, blank=True, verbose_name="После (static)")
    sort_order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Показывать")

    class Meta:
        verbose_name = "Сравнение до/после"
        verbose_name_plural = "Сравнения до/после"
        ordering = ["sort_order", "pk"]

    def __str__(self):
        return self.title

    @property
    def is_ready(self):
        before = bool(self.before_image) or bool(self.before_static)
        after = bool(self.after_image) or bool(self.after_static)
        return before and after


class BlogSection(models.Model):
    badge_text = models.CharField(
        max_length=64, default="ПОЛЕЗНО ЗНАТЬ", verbose_name="Бейдж"
    )
    title_prefix = models.CharField(
        max_length=80, default="Статьи", verbose_name="Заголовок (белая часть)"
    )
    title_highlight = models.CharField(
        max_length=80, default="и советы", verbose_name="Заголовок (акцент)"
    )
    description = models.TextField(
        default=(
            "Полезные материалы о шлифовке, отделке и уходе за деревянным домом — "
            "от специалистов ArteMadera."
        ),
        verbose_name="Описание",
    )
    archive_url = models.CharField(
        max_length=255,
        default="/blog/",
        verbose_name="Ссылка «Все статьи»",
        help_text="Например /blog/ для внутреннего блога",
    )
    archive_link_text = models.CharField(
        max_length=80,
        default="Все статьи блога",
        verbose_name="Текст ссылки на блог",
    )
    is_visible = models.BooleanField(default=True, verbose_name="Показывать блок")

    class Meta:
        verbose_name = "Блок «Блог»"
        verbose_name_plural = "Блок «Блог»"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Блог"


class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True,
        verbose_name="Слаг (URL)",
        help_text="Заполняется автоматически из заголовка. Используется для /blog/<slug>/",
    )
    excerpt = models.TextField(verbose_name="Краткое описание")
    content = models.TextField(
        blank=True,
        verbose_name="Текст статьи",
        help_text="Полный текст статьи (поддерживает HTML). Если заполнен — статья открывается на сайте.",
    )
    url = models.URLField(
        blank=True,
        verbose_name="Внешняя ссылка",
        help_text="Заполните, если статья на внешнем сайте. Если пусто — используется внутренняя страница /blog/<slug>/",
    )
    image = models.ImageField(
        upload_to="blog/",
        blank=True,
        null=True,
        verbose_name="Обложка (загрузка)",
    )
    static_image = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Обложка (static)",
        help_text="Например images/portfolio-1.jpg",
    )
    published_at = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата публикации",
    )
    sort_order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Показывать")

    class Meta:
        verbose_name = "Статья блога"
        verbose_name_plural = "Статьи блога"
        ordering = ["sort_order", "-published_at", "pk"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.slug:
            return f"/blog/{self.slug}/"
        return "/blog/"

    @property
    def is_internal(self):
        return True

    @property
    def has_image(self):
        return bool(self.image) or bool(self.static_image)
