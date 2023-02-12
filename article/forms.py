from django import forms
from article_translation_sample.settings import LANGUAGES
from .models import Article

class ArticleForm(forms.Form):

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for lcode,lstr in LANGUAGES:
            #init fields in form based on settings.LANGUAGES
            #the first language in settings.LANGUAGES, we shall consider as default language hence required
            if lcode==LANGUAGES[0][0]:
                self.fields[lcode] = forms.CharField(label=f"Article in {lstr}",
                required=True)
            else:
                self.fields[lcode] = forms.CharField(label=f"Article in {lstr}",
                initial=None,required=False)


    def save(self):
        """
        Function to be called in POST view to create an new article titles.
        """
        title = { lcode : self.cleaned_data[lcode] for lcode,_ in LANGUAGES}
        article = Article(title=title)
        article.save()
        return article
        
    def update(self,id):
        """
        Function to be called in POST view to create an new article titles.
        """

        article = Article.objects.filter(id = id)
        if not article.exists(): raise forms.ValidationError({"invalid":"Article does not Exists"})
        article=article.first()
        title = { lcode : self.cleaned_data[lcode] for lcode,_ in LANGUAGES}
        article.title=title
        article.save()
        return article
