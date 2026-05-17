from django.db import migrations, models
import django.db.models.deletion


CASE_SEEDS = [
    {
        "static_image": "images/portfolio-1.jpg",
        "title": "Шлифовка сруба в Подмосковье",
        "summary": "Комплексная шлифовка бревенчатого сруба с подготовкой под покраску.",
        "description": (
            "Удалили старое покрытие, выровняли поверхность бревна в несколько проходов "
            "и подготовили дом к нанесению защитного состава. Работы выполнены бригадой "
            "без проживания на объекте."
        ),
        "house_type": "srub",
        "location": "Московская область",
        "work_types": "шлифовка, подготовка под покраску",
        "sort_order": 0,
        "extra_photos": ["images/service-1.jpg", "images/portfolio-2.jpg"],
    },
    {
        "static_image": "images/portfolio-2.jpg",
        "title": "Отделка дома из оцилиндрованного бревна",
        "summary": "Завершили отделку сруба — фасад и подготовка под финишное покрытие.",
        "description": (
            "Объект из оцилиндрованного бревна: шлифовка с сохранением профиля, "
            "контроль влажности и чистовая подготовка под ЛКМ."
        ),
        "house_type": "ocil",
        "location": "Владимирская область",
        "work_types": "шлифовка, отделка",
        "has_before_after": True,
        "sort_order": 1,
        "extra_photos": ["images/portfolio-1.jpg"],
    },
    {
        "static_image": "images/service-2.jpg",
        "title": "Дом из клеёного бруса",
        "summary": "Шлифовка и покраска клеёного бруса — ровная поверхность без сколов.",
        "description": (
            "Закончили отделку дома из клеёного бруса: деликатная шлифовка плоскостей, "
            "удаление пыли, нанесение защитного покрытия по согласованной системе."
        ),
        "house_type": "kleen",
        "location": "Дмитровский г.о.",
        "work_types": "шлифовка, покраска",
        "sort_order": 2,
        "extra_photos": ["images/service-3.jpg"],
    },
    {
        "static_image": "images/service-3.jpg",
        "title": "Баня из рубленного бревна",
        "summary": "Реставрация и шлифовка небольшой бани — готовность к пропитке.",
        "description": (
            "Небольшая баня из рубленного бревна: восстановление древесины, шлифовка "
            "внутри и снаружи с учётом влажностного режима."
        ),
        "house_type": "banya",
        "location": "Солнечногорский район",
        "work_types": "шлифовка, реставрация",
        "sort_order": 3,
        "extra_photos": ["images/portfolio-3.jpg"],
    },
    {
        "static_image": "images/portfolio-3.jpg",
        "title": "Комплексная отделка брусового дома",
        "summary": "Шлифовка и финишная отделка — дом готов к эксплуатации.",
        "description": (
            "Выполнили комплекс работ по отделке брусового дома: подготовка поверхности, "
            "шлифовка, контроль качества на каждом этапе."
        ),
        "house_type": "brus",
        "location": "Калужская область",
        "work_types": "шлифовка, комплекс отделки",
        "sort_order": 4,
        "extra_photos": ["images/service-2.jpg"],
    },
    {
        "static_image": "images/portfolio-2.jpg",
        "title": "Реставрация после недобросовестных подрядчиков",
        "summary": "Переделка фасада и восстановление древесины на объекте.",
        "description": (
            "Взялись за переделку работ: устранили дефекты, провели шлифовку "
            "и подготовили дом к корректному финишному покрытию."
        ),
        "house_type": "srub",
        "location": "Московская область",
        "work_types": "шлифовка, реставрация",
        "has_before_after": True,
        "sort_order": 5,
        "extra_photos": ["images/portfolio-2.jpg", "images/portfolio-1.jpg"],
    },
]


def seed_portfolio_cases(apps, schema_editor):
    PortfolioProject = apps.get_model("main", "PortfolioProject")
    PortfolioProjectImage = apps.get_model("main", "PortfolioProjectImage")

    PortfolioProject.objects.all().update(is_active=False)

    for seed in CASE_SEEDS:
        project, _ = PortfolioProject.objects.update_or_create(
            title=seed["title"],
            defaults={
                "static_image": seed["static_image"],
                "title": seed["title"],
                "summary": seed["summary"],
                "description": seed["description"],
                "house_type": seed["house_type"],
                "location": seed["location"],
                "work_types": seed["work_types"],
                "has_before_after": seed.get("has_before_after", False),
                "sort_order": seed["sort_order"],
                "is_active": True,
                "alt_text": seed["title"],
            },
        )
        PortfolioProjectImage.objects.filter(project=project).delete()
        PortfolioProjectImage.objects.create(
            project=project,
            static_image=seed["static_image"],
            is_cover=True,
            sort_order=0,
            is_active=True,
            caption="Фасад",
        )
        for idx, path in enumerate(seed.get("extra_photos", []), start=1):
            if path == seed["static_image"]:
                continue
            PortfolioProjectImage.objects.create(
                project=project,
                static_image=path,
                is_cover=False,
                sort_order=idx,
                is_active=True,
            )

    for project in PortfolioProject.objects.all():
        if not project.title:
            project.title = project.alt_text or f"Объект #{project.pk}"
        if not project.summary:
            project.summary = project.title[:300]
        project.save(update_fields=["title", "summary"])
        if not PortfolioProjectImage.objects.filter(project=project).exists():
            if project.static_image or project.image:
                PortfolioProjectImage.objects.create(
                    project=project,
                    static_image=project.static_image or "",
                    is_cover=True,
                    sort_order=0,
                    is_active=True,
                )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0007_faq_beforeafter"),
    ]

    operations = [
        migrations.AddField(
            model_name="portfolioproject",
            name="description",
            field=models.TextField(blank=True, verbose_name="Описание (в раскрытии)"),
        ),
        migrations.AddField(
            model_name="portfolioproject",
            name="has_before_after",
            field=models.BooleanField(default=False, verbose_name="Есть серия «До/После»"),
        ),
        migrations.AddField(
            model_name="portfolioproject",
            name="house_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("srub", "Сруб"),
                    ("brus", "Брус"),
                    ("ocil", "Оцилиндровка"),
                    ("banya", "Баня / сауна"),
                    ("kleen", "Клеёный брус"),
                    ("other", "Другое"),
                ],
                max_length=16,
                verbose_name="Тип дома",
            ),
        ),
        migrations.AddField(
            model_name="portfolioproject",
            name="location",
            field=models.CharField(blank=True, max_length=200, verbose_name="Локация"),
        ),
        migrations.AddField(
            model_name="portfolioproject",
            name="summary",
            field=models.CharField(blank=True, max_length=300, verbose_name="Кратко (на карточке)"),
        ),
        migrations.AddField(
            model_name="portfolioproject",
            name="work_types",
            field=models.CharField(
                blank=True,
                help_text="Через запятую: шлифовка, покраска",
                max_length=200,
                verbose_name="Услуги",
            ),
        ),
        migrations.AlterField(
            model_name="portfolioproject",
            name="alt_text",
            field=models.CharField(blank=True, max_length=255, verbose_name="Alt обложки"),
        ),
        migrations.AlterField(
            model_name="portfolioproject",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="portfolio/",
                verbose_name="Обложка (загрузка)",
            ),
        ),
        migrations.AlterField(
            model_name="portfolioproject",
            name="static_image",
            field=models.CharField(
                blank=True,
                help_text="Если нет галереи: images/portfolio-1.jpg",
                max_length=200,
                verbose_name="Обложка (static)",
            ),
        ),
        migrations.AlterField(
            model_name="portfolioproject",
            name="title",
            field=models.CharField(max_length=200, verbose_name="Название кейса"),
        ),
        migrations.AlterModelOptions(
            name="portfolioproject",
            options={"ordering": ["sort_order", "pk"], "verbose_name": "Кейс", "verbose_name_plural": "Кейсы"},
        ),
        migrations.CreateModel(
            name="PortfolioProjectImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(blank=True, null=True, upload_to="portfolio/cases/", verbose_name="Фото")),
                ("static_image", models.CharField(blank=True, max_length=200, verbose_name="Фото (static)")),
                ("caption", models.CharField(blank=True, max_length=200, verbose_name="Подпись")),
                ("is_cover", models.BooleanField(default=False, verbose_name="Обложка")),
                ("sort_order", models.IntegerField(default=0, verbose_name="Порядок")),
                ("is_active", models.BooleanField(default=True, verbose_name="Показывать")),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="photos",
                        to="main.portfolioproject",
                        verbose_name="Кейс",
                    ),
                ),
            ],
            options={
                "verbose_name": "Фото кейса",
                "verbose_name_plural": "Фото кейса",
                "ordering": ["-is_cover", "sort_order", "pk"],
            },
        ),
        migrations.RunPython(seed_portfolio_cases, migrations.RunPython.noop),
    ]
