from django.db import migrations


def refresh_service_card_images(apps, schema_editor):
    Service = apps.get_model("main", "Service")
    HomeQuizSettings = apps.get_model("main", "HomeQuizSettings")

    service_images = {
        # Обсада / окна: убираем одну и ту же картинку с проёмом на все плитки.
        "obsada-okna": ("pages/hero/2316ce5c-b962-41fa-971a-87e9528d1c4a.webp", ""),
        "obsada-dveri": ("pages/hero/2316ce5c-b962-41fa-971a-87e9528d1c4a_yLSXMX6.webp", ""),
        "okosyachka": ("", "images/quiz/quiz_brus_1776809793588.png"),

        # Шлифовка: разные фактуры и процессы вместо повторов/случайной террасы.
        "card-shlifovka-srub": ("", "images/service-1.jpg"),
        "card-shlifovka-brus": ("services/брус_2.webp", ""),
        "card-shlifovka-ocil": ("services/оцилиндовка_2.webp", ""),
        "card-shlifovka-lafet": ("services/лафет.webp", ""),
        "card-shlifovka-pogonazh": ("services/c2bf2ee4-4a5a-4b7d-a660-49c5c9645167.webp", ""),

        # Покраска: фото с нанесением покрытия и готовыми фасадами, не шлифовка.
        "pokraska-outside": ("pages/hero/3efce450-8733-4407-9fee-a220bb2d46b5.webp", ""),
        "pokraska-inside": ("pages/hero/5955e59c-1584-42ec-ac89-d0b1ae9d1f03.webp", ""),
        "pokraska-pogonazh": ("", "images/quiz/quiz_pokraska_1776809864700.png"),
        "pokraska-renewal": ("", "images/service-3.jpg"),

        # Тёплый шов: плитки тоже разводим по более релевантным фото.
        "teplyy-shov-ocil": ("services/оцилиндовка_2.webp", ""),
        "teplyy-shov-brus": ("services/брус_2.webp", ""),
        "teplyy-shov-preserve": ("pages/hero/23b84e30-5a9c-45b5-acca-0462e07d96e2.webp", ""),
    }
    for slug, (image, static_image) in service_images.items():
        Service.objects.filter(slug=slug).update(
            image=image,
            static_image=static_image,
        )

    quiz, _ = HomeQuizSettings.objects.get_or_create(pk=1)
    quiz.image_shlifovka = "pages/hero/137908e0-151b-425d-9233-b2af8fca286d.webp"
    quiz.image_pokraska = "pages/hero/3efce450-8733-4407-9fee-a220bb2d46b5.webp"
    quiz.image_obsada = "pages/hero/2316ce5c-b962-41fa-971a-87e9528d1c4a.webp"
    quiz.image_okosyachka = "pages/hero/2316ce5c-b962-41fa-971a-87e9528d1c4a_zI05m1D.webp"
    quiz.save(update_fields=[
        "image_shlifovka",
        "image_pokraska",
        "image_obsada",
        "image_okosyachka",
    ])


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0058_update_teplyy_shov_service_tiles"),
    ]

    operations = [
        migrations.RunPython(refresh_service_card_images, noop_reverse),
    ]
