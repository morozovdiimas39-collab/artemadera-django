from django import forms

from .models import SitePage


class SitePageAdminForm(forms.ModelForm):
    class Meta:
        model = SitePage
        fields = "__all__"
        labels = {
            "hero_image": "Фоновое изображение",
        }
        help_texts = {
            "hero_image": (
                "Нажмите иконку загрузки справа от поля, выберите картинку с компьютера "
                "(JPG, PNG, WebP) и обязательно нажмите «Сохранить» внизу страницы."
            ),
        }
