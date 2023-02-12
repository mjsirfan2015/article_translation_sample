from django.db import models
from django import forms
from article_translation_sample import settings
# Create your models here.

class LanguageNotFoundError(Exception):
    message="Language is not defined settings.LANGUAGES"

class Article(models.Model):

    def save(self, *args, **kwargs):
        if not isinstance(self.title,dict): 
            #make sure self.title is dictionary
            raise TypeError(dict)
        inp_keys = set(self.title.keys())
        lang_keys = set([lcode for lcode,_ in settings.LANGUAGES])
        if not inp_keys.intersection(lang_keys):
            #raise error if any other keys are present
            raise LanguageNotFoundError()
        return super().save(*args, **kwargs)

    title = models.JSONField("Article Title",default=dict)
