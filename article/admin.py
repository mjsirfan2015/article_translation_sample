
from django.contrib import admin
from django import forms
from .models import Article
from article_translation_sample.settings import LANGUAGES
from django.utils.translation import gettext_lazy as _


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', *[lang[0] for lang in LANGUAGES])

    def __getattribute__(self, name):
        if name in [lang[0] for lang in LANGUAGES]:
            def list_display_method(obj):
                return obj.title.get(name, None)
            list_display_method.short_description = f"Article Title ({name})"
            return list_display_method
        return super().__getattribute__(name)

admin.site.register(Article, ArticleAdmin)

