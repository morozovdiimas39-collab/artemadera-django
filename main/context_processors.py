import json
from types import SimpleNamespace

from django.db.utils import OperationalError

from .models import (
    Service,
    CalculatorConfig,
    CalculatorMaterial,
    PortfolioSection,
    PortfolioProject,
    ExperienceSection,
    ExperienceStat,
    ExperienceAdvantage,
    ReviewsSection,
    Review,
    WorkProcessSection,
    WorkProcessStep,
    ContactSection,
    FaqSection,
    FaqItem,
    BeforeAfterSection,
    BeforeAfterItem,
    BlogSection,
    BlogPost,
    SitePage,
)


def _format_rub(amount):
    return f"{int(amount):,}".replace(",", "\u00a0") + " \u20bd"


def _calculator_defaults():
    from .calculator_service import _legacy_context

    return _legacy_context()


def _home_services_defaults():
    """Fallback if DB empty — mirrors migration seed (tags/prices from calculator slugs)."""
    from .models import CalculatorProfile

    seeds = [
        ("shlifovka", "Шлифовка деревянных домов", "Срубы, брус, оцилиндровка и лафет.", "/shlifovka", "wide", "", "images/quiz/quiz_shlifovka_1776809850085.png"),
        ("pokraska", "Покраска", "Грунт, масла и лазури для фасада и интерьера.", "/pokraska", "", "под ключ", "images/quiz/quiz_pokraska_1776809864700.png"),
        ("teplyy-shov", "Тёплый шов", "Заполнение межвенцовых швов эластичным составом.", "/teplyy-shov", "", "герметизация", "images/quiz/quiz_konopatka_1776809894304.png"),
        ("okosyachka", "Окосячка", "Компенсация усадки, углы и каркас сруба.", "/obsada", "", "усадка", "images/quiz/quiz_srub_1776809774832.png"),
        ("obsada-okna", "Обсада", "Короба под окна и двери.", "/obsada/okna", "", "проёмы", "images/quiz/quiz_brus_1776809793588.png"),
        ("kryshi", "Крыши", "Монтаж и ремонт кровли.", "/kryshi", "", "кровля", "images/portfolio-3.jpg"),
        ("injeneriya", "Инженерия", "Проект и монтаж инженерных систем.", "/injeneriya", "last", "коммуникации", "images/after.jpg"),
    ]
    calc_slugs = {
        "shlifovka": "shlifovka",
        "pokraska": "pokraska",
        "teplyy-shov": "teplyy-shov",
        "okosyachka": "obsada",
        "obsada-okna": "obsada",
        "kryshi": "kryshi",
        "injeneriya": "injeneriya",
    }
    profiles = {}
    try:
        for p in CalculatorProfile.objects.filter(slug__in=set(calc_slugs.values())):
            profiles[p.slug] = p
    except OperationalError:
        pass

    items = []
    for slug, name, desc, url, layout, tag_override, static_image in seeds:
        calc_slug = calc_slugs.get(slug, slug)
        calc = profiles.get(calc_slug)
        tag = tag_override
        if not tag and calc:
            tag = calc.home_price_tag()
        items.append(
            SimpleNamespace(
                name=name,
                short_description=desc,
                link_url=url,
                home_layout=layout,
                get_home_tag=lambda t=tag: t,
                has_image=True,
                image=None,
                static_image=static_image,
            )
        )
    return items


class _ShlifovkaFallbackCard:
    """Те же поля, что у _ServiceCard, если в БД ещё нет привязок для /shlifovka."""

    __slots__ = (
        "name",
        "short_description",
        "link_url",
        "home_layout",
        "static_image",
        "image",
        "cta_label",
        "_tag",
    )

    def __init__(
        self,
        *,
        name,
        short_description,
        link_url,
        home_layout,
        tag,
        static_image,
        cta_label="",
    ):
        self.name = name
        self.short_description = short_description
        self.link_url = link_url
        self.home_layout = home_layout
        self.static_image = static_image
        self.image = None
        self.cta_label = (cta_label or "").strip()
        self._tag = tag

    def get_home_tag(self):
        return self._tag


def _shlifovka_services_defaults():
    rows = [
        {
            "name": "Шлифовка срубов",
            "short_description": (
                "Шлифовка бревенчатых срубов: удаление старого покрытия, "
                "выравнивание и подготовка под финиш."
            ),
            "link_url": "/otdelka/shlifovka/sruba",
            "static_image": "images/service-1.jpg",
            "home_layout": "wide",
            "tag": "от 1 200 ₽/м²",
        },
        {
            "name": "Шлифовка бруса",
            "short_description": (
                "Шлифовка домов из профилированного и клееного бруса без повреждения геометрии."
            ),
            "link_url": "/otdelka/shlifovka/brusa",
            "static_image": "images/service-2.jpg",
            "home_layout": "",
            "tag": "от 1 100 ₽/м²",
        },
        {
            "name": "Шлифовка оцилиндровки",
            "short_description": (
                "Шлифовка дома из оцилиндрованного бревна с сохранением естественной фактуры дерева."
            ),
            "link_url": "/otdelka/shlifovka/ocilindrovannogo-brevna",
            "static_image": "images/portfolio-1.jpg",
            "home_layout": "",
            "tag": "от 1 150 ₽/м²",
        },
        {
            "name": "Шлифовка лафета",
            "short_description": (
                "Аккуратная шлифовка домов из лафета и плоскогранного бруса — ровная поверхность без сколов."
            ),
            "link_url": "/otdelka/shlifovka/lafeta",
            "static_image": "images/portfolio-2.jpg",
            "home_layout": "wide",
            "tag": "от 1 250 ₽/м²",
        },
        {
            "name": "Консьержная шлифовка",
            "short_description": (
                "Финишная тонкая шлифовка перед покраской или пропиткой — идеально гладкая поверхность."
            ),
            "link_url": "/otdelka/shlifovka/konsyerzhnaya",
            "static_image": "images/service-3.jpg",
            "home_layout": "half",
            "tag": "от 800 ₽/м²",
        },
        {
            "name": "Шлифовка бань и саун",
            "short_description": (
                "Шлифовка деревянных бань и саун с учётом высоких температур и влажности."
            ),
            "link_url": "/otdelka/shlifovka/bani-i-sauny",
            "static_image": "images/portfolio-3.jpg",
            "home_layout": "half",
            "tag": "от 900 ₽/м²",
            "cta_label": "Рассчитать стоимость",
        },
    ]
    return [_ShlifovkaFallbackCard(**{**r, "cta_label": r.get("cta_label", "")}) for r in rows]


def _service_cards_grid_mode(cards):
    """
    equal — до 4 карточек без wide/half/last: фиксированные колонки.
    twelve — иначе сетка 12 колонок с col-span (как было на шлифовке).
    """
    if not cards:
        return "twelve"
    if len(cards) > 4:
        return "twelve"
    for c in cards:
        if (getattr(c, "home_layout", None) or "").strip():
            return "twelve"
    return "equal"


def _service_cards_dense_order(cards):
    """Внутренние страницы: сохраняем порядок из админки, чтобы wide-карточки собирали ритм как на шлифовке."""
    return list(cards or [])


def services_processor(request):
    from .site_page import (
        get_page_service_cards,
        get_shlifovka_page_service_cards,
        normalize_page_key,
    )

    page_key = normalize_page_key(request.path)
    try:
        services = Service.objects.filter(is_active=True).order_by("order")
        home_services = get_page_service_cards("home")
        shlifovka_page_services = get_shlifovka_page_service_cards()
        page_service_cards = get_page_service_cards(page_key)
    except OperationalError:
        services = []
        home_services = []
        shlifovka_page_services = []
        page_service_cards = []
    if not home_services:
        home_services = _home_services_defaults()
    if not shlifovka_page_services:
        shlifovka_page_services = _shlifovka_services_defaults()
    page_service_cards = _service_cards_dense_order(page_service_cards)
    return {
        "all_services": services,
        "home_services": home_services,
        "shlifovka_page_services": shlifovka_page_services,
        "shlifovka_services_grid_mode": _service_cards_grid_mode(shlifovka_page_services),
        "page_service_cards": page_service_cards,
        "page_services_grid_mode": _service_cards_grid_mode(page_service_cards),
    }


def calculator_processor(request):
    from .calculator_service import build_calculator_context

    try:
        return build_calculator_context(request)
    except Exception:
        return _calculator_defaults()


def _portfolio_case_namespace(pk, seed):
    photos = [
        SimpleNamespace(
            image=None,
            static_image=path,
            caption="",
            is_cover=(idx == 0),
        )
        for idx, path in enumerate(seed.get("photos", [])[:3])
    ]
    project = SimpleNamespace(
        pk=pk,
        title=seed["title"],
        summary=seed.get("summary", ""),
        description=seed.get("description", ""),
        house_type=seed.get("house_type", ""),
        house_type_label=seed.get("house_type_label", ""),
        location=seed.get("location", ""),
        work_types=seed.get("work_types", ""),
        work_types_list=seed.get("work_types_list", []),
        has_before_after=seed.get("has_before_after", False),
        image=None,
        static_image=seed["photos"][0] if seed.get("photos") else "",
        alt_text=seed["title"],
        sort_order=seed.get("sort_order", 0),
        is_active=True,
        photos=photos,
    )

    def get_gallery_items():
        return photos or [project]

    def cover_item():
        return photos[0] if photos else project

    project.get_gallery_items = get_gallery_items
    project.cover_item = cover_item
    project.has_image = True
    return project


def _portfolio_defaults():
    section = SimpleNamespace(
        badge_text="ПОРТФОЛИО",
        title_prefix="Наши",
        title_highlight="проекты",
        description=(
            "Оцените качество нашей работы: реальные объекты — шлифовка, отделка "
            "и восстановление деревянных домов в Москве и области."
        ),
        is_visible=True,
    )
    seeds = [
        {
            "title": "Шлифовка сруба в Подмосковье",
            "summary": "Комплексная шлифовка бревенчатого сруба с подготовкой под покраску.",
            "description": "Удалили старое покрытие, выровняли поверхность и подготовили дом к ЛКМ.",
            "house_type": "srub",
            "house_type_label": "Сруб",
            "location": "Московская область",
            "work_types": "шлифовка, подготовка под покраску",
            "work_types_list": ["шлифовка", "подготовка под покраску"],
            "photos": ["images/portfolio-1.jpg", "images/portfolio-2.jpg"],
            "sort_order": 0,
        },
        {
            "title": "Отделка дома из оцилиндрованного бревна",
            "summary": "Завершили отделку сруба — фасад и подготовка под финиш.",
            "description": "Шлифовка с сохранением профиля бревна и контроль влажности на объекте.",
            "house_type": "ocil",
            "house_type_label": "Оцилиндровка",
            "location": "Владимирская область",
            "work_types": "шлифовка, отделка",
            "work_types_list": ["шлифовка", "отделка"],
            "has_before_after": True,
            "photos": ["images/portfolio-2.jpg", "images/service-1.jpg"],
            "sort_order": 1,
        },
        {
            "title": "Дом из клеёного бруса",
            "summary": "Шлифовка и покраска — ровная поверхность без сколов.",
            "description": "Закончили отделку дома из клеёного бруса по согласованной системе покрытий.",
            "house_type": "kleen",
            "house_type_label": "Клеёный брус",
            "location": "Дмитровский г.о.",
            "work_types": "шлифовка, покраска",
            "work_types_list": ["шлифовка", "покраска"],
            "photos": ["images/service-2.jpg", "images/service-3.jpg"],
            "sort_order": 2,
        },
        {
            "title": "Баня из рубленного бревна",
            "summary": "Реставрация и шлифовка бани — готовность к пропитке.",
            "description": "Восстановление древесины внутри и снаружи с учётом влажностного режима.",
            "house_type": "banya",
            "house_type_label": "Баня / сауна",
            "location": "Солнечногорский район",
            "work_types": "шлифовка, реставрация",
            "work_types_list": ["шлифовка", "реставрация"],
            "photos": ["images/service-3.jpg", "images/portfolio-3.jpg"],
            "sort_order": 3,
        },
    ]
    projects = [_portfolio_case_namespace(i + 1, s) for i, s in enumerate(seeds)]
    return {"portfolio_section": section, "portfolio_projects": projects}


def portfolio_processor(request):
    try:
        section = PortfolioSection.load()
        projects = list(
            PortfolioProject.objects.filter(is_active=True)
            .prefetch_related("photos")
            .order_by("sort_order", "pk")
        )
        projects = [p for p in projects if p.has_image]
    except OperationalError:
        return _portfolio_defaults()

    if not section.is_visible:
        return {"portfolio_section": section, "portfolio_projects": []}

    if not projects:
        return _portfolio_defaults()

    return {"portfolio_section": section, "portfolio_projects": projects}


def _experience_defaults():
    section = SimpleNamespace(
        badge_text="ОПЫТ И НАДЁЖНОСТЬ",
        title_prefix="Более",
        title_highlight="10 лет с деревом",
        description=(
            "Строительно-отделочная компания полного цикла для деревянных домов "
            "в Москве и области — от шлифовки и покраски до кровли и инженерии."
        ),
        story=(
            "ArteMadera объединяет комплекс отделочных работ у одного исполнителя: "
            "не нужно искать разных подрядчиков и согласовывать сроки. Работаем по договору "
            "с фиксированной сметой, используем сертифицированные материалы и собственное "
            "производство. На замере можем бесплатно показать качество — «тест-драйв» "
            "на участке вашего дома."
        ),
        image=None,
        static_image="images/team.png",
        is_visible=True,
    )
    stats = [
        SimpleNamespace(value="10+", label="Лет на рынке"),
        SimpleNamespace(value="500+", label="Выполненных объектов"),
        SimpleNamespace(value="1", label="Подрядчик на весь цикл"),
        SimpleNamespace(value="3 года", label="Гарантия на работы"),
    ]
    advantages = [
        SimpleNamespace(
            title="Работа по договору",
            description="Фиксируем обязательства и гарантию в договоре.",
            icon="contract",
        ),
        SimpleNamespace(
            title="Смета без «раздуваний»",
            description="Согласованный бюджет не меняется в процессе работ.",
            icon="wallet",
        ),
        SimpleNamespace(
            title="Тест-драйв качества",
            description="Бесплатно показываем технологию на замере.",
            icon="sparkles",
        ),
        SimpleNamespace(
            title="Собственное производство",
            description="Плинтусы, фальшбалки и другие элементы — под контролем.",
            icon="factory",
        ),
    ]
    return {
        "experience_section": section,
        "experience_stats": stats,
        "experience_advantages": advantages,
    }


def experience_processor(request):
    try:
        section = ExperienceSection.load()
        stats = list(
            ExperienceStat.objects.filter(is_active=True).order_by("sort_order", "pk")
        )
        advantages = list(
            ExperienceAdvantage.objects.filter(is_active=True).order_by(
                "sort_order", "pk"
            )
        )
    except OperationalError:
        return _experience_defaults()

    if not section.is_visible:
        return {
            "experience_section": section,
            "experience_stats": [],
            "experience_advantages": [],
        }

    if not section.image and section.static_image in (
        "images/service-2.jpg",
        "images/hero-bg.jpg",
        "images/after.jpg",
    ):
        section.static_image = "images/team.png"

    defaults = _experience_defaults()
    return {
        "experience_section": section,
        "experience_stats": stats or defaults["experience_stats"],
        "experience_advantages": advantages or defaults["experience_advantages"],
    }


def _reviews_defaults():
    section = SimpleNamespace(
        badge_text="ОТЗЫВЫ",
        title_prefix="Что говорят",
        title_highlight="клиенты",
        description=(
            "Реальные отзывы с Яндекс.Карт и сайта ArteMadera — о шлифовке, "
            "отделке и работе команды на объекте."
        ),
        yandex_maps_url="https://yandex.ru/maps/org/artemadera/45828270851/",
        yandex_rating=5.0,
        yandex_reviews_count=0,
        is_visible=True,
    )
    reviews = [
        SimpleNamespace(
            author_name="Ольга Б.",
            headline="Финский стиль",
            text=(
                "Ребята из «ArteMadera» умеют слышать потребности заказчика. Только здесь поняли нашу идею "
                "строений в финском стиле и выполнили очень сложную задачу с отличным качеством."
            ),
            rating=5,
            source="yandex",
        ),
        SimpleNamespace(
            author_name="Иваныч",
            headline="Рекомендую ArteMadera",
            text="Ребята работают чётко, быстро, слаженно, а главное — честно и открыто.",
            rating=5,
            source="yandex",
        ),
        SimpleNamespace(
            author_name="Пётр",
            headline="Дом из бруса",
            text="В 2020 году построили двухэтажный брусовой дом на сложных почвах — результатом остались довольны.",
            rating=5,
            source="yandex",
        ),
        SimpleNamespace(
            author_name="Александр К.",
            headline="Лучший менеджер",
            text="Безупречное, добросовестное отношение менеджеров ArteMadera — спасибо за сопровождение!",
            rating=5,
            source="yandex",
        ),
        SimpleNamespace(
            author_name="Константин",
            headline="Дом мечты",
            text="Дом собрали очень качественно и быстро. Получилось именно то, что хотели.",
            rating=5,
            source="yandex",
        ),
        SimpleNamespace(
            author_name="Татьяна",
            headline="Остались довольны",
            text="Замечательная фирма, строят уже не первый год. Я довольна сотрудничеством.",
            rating=5,
            source="yandex",
        ),
    ]
    return {"reviews_section": section, "site_reviews": reviews}


def reviews_processor(request):
    try:
        section = ReviewsSection.load()
        reviews = list(
            Review.objects.filter(is_active=True).order_by("sort_order", "pk")
        )
    except OperationalError:
        return _reviews_defaults()

    if not section.is_visible:
        return {"reviews_section": section, "site_reviews": []}

    if not reviews:
        return _reviews_defaults()

    return {"reviews_section": section, "site_reviews": reviews}


def _process_defaults():
    section = SimpleNamespace(
        badge_text="КАК МЫ РАБОТАЕМ",
        title_prefix="Этапы",
        title_highlight="нашей работы",
        description=(
            "От первого выезда до передачи объекта — четыре последовательных шага, "
            "понятных ещё до начала работ."
        ),
        is_visible=True,
    )
    steps = [
        SimpleNamespace(
            step_number="01",
            title="Выезд на объект",
            description=(
                "Осматриваем задачу и объём: замеры, фото, фиксация пожеланий — отправная точка для сметы."
            ),
        ),
        SimpleNamespace(
            step_number="02",
            title="Смета и договор",
            description=(
                "Считаем работы по этапам, согласуем сроки и цену, закрепляем всё в договоре — без скрытых условий."
            ),
        ),
        SimpleNamespace(
            step_number="03",
            title="Работы на объекте",
            description=(
                "Выполняем этапы по плану: технология, безопасность, порядок и промежуточные согласования по ходу."
            ),
        ),
        SimpleNamespace(
            step_number="04",
            title="Сдача объекта",
            description=(
                "Передаём результат: совместная приёмка, акты, рекомендации по уходу и гарантия на выполненные работы."
            ),
        ),
    ]
    return {"work_process_section": section, "work_process_steps": steps}


def work_process_processor(request):
    try:
        section = WorkProcessSection.load()
        steps = list(
            WorkProcessStep.objects.filter(is_active=True).order_by("sort_order", "pk")
        )
    except OperationalError:
        return _process_defaults()

    if not section.is_visible:
        return {"work_process_section": section, "work_process_steps": []}

    if not steps:
        return _process_defaults()

    return {"work_process_section": section, "work_process_steps": steps}


def _contact_defaults():
    return {
        "contact_section": SimpleNamespace(
            badge_text="СВЯЗАТЬСЯ",
            title_prefix="Оставьте",
            title_highlight="заявку",
            description="Расскажите о доме — перезвоним в течение 30 минут.",
            phone="+7 (495) 005-01-45",
            phone_href="74950050145",
            email="info@artemadera.ru",
            work_hours="Пн–Пт, 9:00–21:00",
            address="г. Москва, м. ВДНХ, Ярославская ул., д. 8, корп. 6, офис 220",
            submit_button_text="Отправить заявку",
            privacy_note="Нажимая кнопку, вы соглашаетесь с обработкой персональных данных",
            is_visible=True,
        )
    }


def contact_processor(request):
    try:
        section = ContactSection.load()
    except OperationalError:
        return _contact_defaults()

    if not section.is_visible:
        return {"contact_section": section}

    return {"contact_section": section}


def _faq_defaults():
    section = SimpleNamespace(
        badge_text="ВОПРОСЫ",
        title_prefix="Частые",
        title_highlight="вопросы",
        description="Ответы на популярные вопросы о шлифовке деревянных домов.",
        is_visible=True,
    )
    items = [
        SimpleNamespace(
            question="Можно ли шлифовать деревянный дом зимой?",
            answer=(
                "Да. На объекте создаём временный тепловой контур, чтобы поддерживать "
                "нужную температуру и влажность."
            ),
        ),
        SimpleNamespace(
            question="Сколько длится шлифовка дома?",
            answer=(
                "Срок зависит от площади и состояния древесины. "
                "Точные сроки фиксируем в смете после замера."
            ),
        ),
    ]
    return {"faq_section": section, "faq_items": items}


def faq_processor(request):
    try:
        section = FaqSection.load()
        items = list(FaqItem.objects.filter(is_active=True).order_by("sort_order", "pk"))
    except OperationalError:
        return _faq_defaults()

    if not section.is_visible:
        return {"faq_section": section, "faq_items": []}

    if not items:
        return _faq_defaults()

    return {"faq_section": section, "faq_items": items}


def _before_after_attach_src(item):
    """URL для <img>: загрузка из админки или путь в static."""
    from django.templatetags.static import static

    if getattr(item, "before_image", None):
        before_src = item.before_image.url
    else:
        p = (getattr(item, "before_static", None) or "").strip() or "images/before.jpg"
        before_src = static(p)
    if getattr(item, "after_image", None):
        after_src = item.after_image.url
    else:
        p = (getattr(item, "after_static", None) or "").strip() or "images/after.jpg"
        after_src = static(p)
    item.before_src = before_src
    item.after_src = after_src


def _before_after_defaults():
    from django.templatetags.static import static

    section = SimpleNamespace(
        badge_text="РЕЗУЛЬТАТ",
        title_prefix="До и",
        title_highlight="после",
        description="Сравните состояние древесины до и после профессиональной шлифовки.",
        is_visible=True,
    )
    items = [
        SimpleNamespace(
            pk=1,
            title="Шлифовка сруба",
            before_image=None,
            after_image=None,
            before_static="images/before.jpg",
            after_static="images/after.jpg",
            is_active=True,
            is_ready=True,
            before_src=static("images/before.jpg"),
            after_src=static("images/after.jpg"),
        ),
    ]
    return {"before_after_section": section, "before_after_items": items}


def before_after_processor(request):
    from .site_page import normalize_page_key

    before_after_page_key = normalize_page_key(request.path)
    try:
        section = BeforeAfterSection.load()
        page = SitePage.objects.filter(
            page_key=before_after_page_key, is_active=True
        ).first()
        home_page = SitePage.objects.filter(page_key="home", is_active=True).first()
        page_items = []
        if page:
            page_items = list(
                BeforeAfterItem.objects.filter(page=page, is_active=True).order_by(
                    "sort_order", "pk"
                )
            )
        home_items = []
        if home_page and before_after_page_key == "home":
            home_items = list(
                BeforeAfterItem.objects.filter(page=home_page, is_active=True).order_by(
                    "sort_order", "pk"
                )
            )
        items = page_items or home_items or list(
            BeforeAfterItem.objects.filter(page__isnull=True, is_active=True).order_by(
                "sort_order", "pk"
            )
        )
        items = [i for i in items if i.is_ready][:2]
    except OperationalError:
        return _before_after_defaults()

    if not section.is_visible:
        return {"before_after_section": section, "before_after_items": []}

    if not items:
        return _before_after_defaults()

    for item in items:
        _before_after_attach_src(item)

    return {"before_after_section": section, "before_after_items": items}


def _blog_defaults():
    section = SimpleNamespace(
        badge_text="ПОЛЕЗНО ЗНАТЬ",
        title_prefix="Статьи",
        title_highlight="и советы",
        description=(
            "Полезные материалы о шлифовке, отделке и уходе за деревянным домом — "
            "от специалистов ArteMadera."
        ),
        archive_url="/blog/",
        archive_link_text="Все статьи блога",
        is_visible=True,
    )
    def _make_post(pk, title, excerpt, slug, static_image):
        ns = SimpleNamespace(
            pk=pk, title=title, excerpt=excerpt,
            url="", slug=slug, image=None, static_image=static_image,
            published_at=None, has_image=True, is_internal=True,
        )
        _slug = slug
        ns.get_absolute_url = lambda: f"/blog/{_slug}/"
        return ns

    posts = [
        _make_post(1, "Можно ли шлифовать сруб зимой?",
            "Как создают тепловой контур на объекте и почему профессиональная шлифовка "
            "возможна не только в тёплый сезон.",
            "mozhno-li-shlifovat-srub-zimoy", "images/quiz/quiz_shlifovka_1776809850085.png"),
        _make_post(2, "Что такое «тёплый шов» для деревянного дома",
            "Зачем нужен эластичный герметик в межвенцовых швах и как он защищает древесину.",
            "chto-takoe-teplyy-shov", "images/quiz/quiz_konopatka_1776809894304.png"),
        _make_post(3, "Как подготовить дом из бруса к покраске",
            "Этапы шлифовки, удаления пыли и выбора системы покрытия для фасада.",
            "kak-podgotovit-dom-iz-brusa-k-pokraske", "images/quiz/quiz_pokraska_1776809864700.png"),
    ]
    return {"blog_section": section, "blog_posts": posts}


def blog_processor(request):
    try:
        section = BlogSection.load()
        posts = list(
            BlogPost.objects.filter(is_active=True).order_by("sort_order", "-published_at", "pk")
        )
    except OperationalError:
        return _blog_defaults()

    if not section.is_visible:
        return {"blog_section": section, "blog_posts": []}

    if not posts:
        return _blog_defaults()

    return {"blog_section": section, "blog_posts": posts}


def site_page_processor(request):
    from .site_page import get_site_page, services_block_captions

    page = get_site_page(request)
    return {
        "site_page": page,
        "page_hero": page,
        "services_block_captions": services_block_captions(page),
    }


# (data-value кнопки, атрибут HomeQuizSettings, путь в static при пустой загрузке)
_HOME_QUIZ_IMAGE_ROWS = [
    ("shlifovka", "image_shlifovka", "images/quiz/quiz_shlifovka_1776809850085.png"),
    ("pokraska", "image_pokraska", "images/quiz/quiz_pokraska_1776809864700.png"),
    ("teplyy-shov", "image_teplyy_shov", "images/quiz/quiz_konopatka_1776809894304.png"),
    ("okosyachka", "image_okosyachka", "images/quiz/quiz_srub_1776809774832.png"),
    ("obsada", "image_obsada", "images/quiz/quiz_brus_1776809793588.png"),
    ("kryshi", "image_kryshi", "images/portfolio-3.jpg"),
    ("injeneriya", "image_injeneriya", "images/after.jpg"),
]
_HOME_QUIZ_DEFAULT_STATIC = "images/hero-bg.jpg"


def _home_quiz_fallback_urls():
    """Те же пути, что раньше были в шаблоне квиза (static)."""
    from django.templatetags.static import static

    return {
        "home_quiz_default_url": static(_HOME_QUIZ_DEFAULT_STATIC),
        "home_quiz_service_images": [
            {"key": k, "url": static(p)} for k, _attr, p in _HOME_QUIZ_IMAGE_ROWS
        ],
    }


def home_quiz_processor(request):
    from django.templatetags.static import static

    from .models import HomeQuizSettings

    fb = _home_quiz_fallback_urls()

    def pick_url(field, static_path):
        if field:
            return field.url
        return static(static_path)

    try:
        cfg = HomeQuizSettings.load()
    except OperationalError:
        return fb

    default_url = pick_url(cfg.default_image, _HOME_QUIZ_DEFAULT_STATIC)
    rows = [
        {"key": data_key, "url": pick_url(getattr(cfg, attr, None), static_path)}
        for data_key, attr, static_path in _HOME_QUIZ_IMAGE_ROWS
    ]

    return {
        "home_quiz_default_url": default_url,
        "home_quiz_service_images": rows,
    }
