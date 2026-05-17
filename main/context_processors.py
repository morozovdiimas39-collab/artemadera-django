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
)


def _format_rub(amount):
    return f"{int(amount):,}".replace(",", "\u00a0") + " \u20bd"


def _calculator_defaults():
    from .calculator_service import _legacy_context

    return _legacy_context()


def services_processor(request):
    try:
        services = Service.objects.filter(is_active=True).order_by('order')
    except OperationalError:
        services = []
    return {'all_services': services}


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
        static_image="images/hero-bg.jpg",
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

    if not section.image and section.static_image == "images/service-2.jpg":
        section.static_image = "images/hero-bg.jpg"

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
        description="Прозрачный и отлаженный процесс — от первого звонка до сдачи готового объекта.",
        is_visible=True,
    )
    steps = [
        SimpleNamespace(
            step_number="01",
            title="Замер и выкрас",
            description="Бесплатная тестовая покраска на вашем доме при замере.",
        ),
        SimpleNamespace(
            step_number="02",
            title="Без проживания",
            description="Мобильные бригады — без необходимости предоставлять жильё.",
        ),
        SimpleNamespace(
            step_number="03",
            title="Честная цена",
            description="Фиксированная смета в договоре без изменений.",
        ),
        SimpleNamespace(
            step_number="04",
            title="Многоуровневый контроль",
            description="Контроль качества на каждом этапе работ.",
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


def _before_after_defaults():
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
        ),
    ]
    return {"before_after_section": section, "before_after_items": items}


def before_after_processor(request):
    try:
        section = BeforeAfterSection.load()
        items = list(
            BeforeAfterItem.objects.filter(is_active=True).order_by("sort_order", "pk")
        )
        items = [i for i in items if i.is_ready]
    except OperationalError:
        return _before_after_defaults()

    if not section.is_visible:
        return {"before_after_section": section, "before_after_items": []}

    if not items:
        return _before_after_defaults()

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
        archive_url="https://artemadera.ru/blog/",
        archive_link_text="Все статьи блога",
        is_visible=True,
    )
    posts = [
        SimpleNamespace(
            pk=1,
            title="Можно ли шлифовать сруб зимой?",
            excerpt=(
                "Как создают тепловой контур на объекте и почему профессиональная шлифовка "
                "возможна не только в тёплый сезон."
            ),
            url="https://artemadera.ru/blog/",
            image=None,
            static_image="images/portfolio-2.jpg",
            published_at=None,
            has_image=True,
        ),
        SimpleNamespace(
            pk=2,
            title='Что такое «тёплый шов» для деревянного дома',
            excerpt=(
                "Зачем нужен эластичный герметик в межвенцовых швах и как он защищает древесину."
            ),
            url="https://artemadera.ru/blog/",
            image=None,
            static_image="images/service-1.jpg",
            published_at=None,
            has_image=True,
        ),
        SimpleNamespace(
            pk=3,
            title="Как подготовить дом из бруса к покраске",
            excerpt="Этапы шлифовки, удаления пыли и выбора системы покрытия для фасада.",
            url="https://artemadera.ru/blog/",
            image=None,
            static_image="images/service-2.jpg",
            published_at=None,
            has_image=True,
        ),
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
