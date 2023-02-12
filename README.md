
Below is the implementation of `models.py` Similar to that mentioned in the document itself; except for a minor difference that is **checking if incoming data is a dictionary** and that language codes/keys other than those mentioned in `settings.LANGUAGES` is not present.

### models.py
```python
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

```
The views below implements an interface to view add and update articles and their titles.

### views.py
```python
from django.shortcuts import render
from django.http import Http404,HttpResponseBadRequest,HttpResponseRedirect
from django.urls import reverse
from .models import Article
from django.views import View
from .forms import ArticleForm
from article_translation_sample.settings import LANGUAGES
# Create your views here.

def display_title_table(request):
    if request.method=="GET":
        articles = Article.objects.all()
        return render(request,"display_form.html",context={"articles":articles,"LANGUAGES":LANGUAGES})

class ArticleModView(View):

    def get(self,request,id=None):
        article = None
        if id is not None:
            article = Article.objects.filter(id=id)
            if not article.exists():return Http404()
        return render(request,'mod_form.html',context={'LANGUAGES':LANGUAGES,'id':id,'article':article and article.first()})
    
    def post(self,request,id=None):
        form = ArticleForm(request.POST)
        if id==None:
            """
                Create new article
            """
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('display_title_table'))
        else:
            """
                Update Article with id 'id'
            """
            article = Article.objects.filter(id=id)
            if not article.exists():return Http404()
            if form.is_valid():
                form.update(id)
                return HttpResponseRedirect(reverse('display_title_table'))
        return  HttpResponseBadRequest(str(form.errors))
```
The form below adds fields dynamically based on values in `settings.LANGUAGES` at any time.Hence the form can be used to extract the data from `request.POST` in above views to  language fields and then update/create article objects.
### forms.py
```python
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

```
The user interface below displays the articles. We use `settings.LANGUAGES` to extract the fields from title field of each article object. On clicking each entry we are redirected to the update page where **text input entries are generated dynamically from** `settings.LANGUAGES`. If instead we click the add button we are redirected to the article creation page which also generates input text fields dynamically.

##### localhost:8000/
![Article Display page]([readme_assets\image1.png](https://media.githubusercontent.com/media/mjsirfan2015/article_translation_sample/main/readme_assets/image1.png) "Article Display page")
##### Article Display page
#
##### localhost:8000/article/1
![Update Existing Article page]([readme_assets\image2.png](https://media.githubusercontent.com/media/mjsirfan2015/article_translation_sample/main/readme_assets/image2.png) "[Update Existing Article page")
##### Update Existing Article page (Notice the page fetches current entries from entry to be updated)
#
##### localhost:8000/article/
![Create new Article page]([readme_assets\image3.png](https://media.githubusercontent.com/media/mjsirfan2015/article_translation_sample/main/readme_assets/image3.png) "Create new Article page")
##### Create new Article page
#
>Also one other possible thing that can be done would be make `settings.LANGUAGES` parameter itself dynamic, by storing the language info in a database rather than settings configuration, so that an admin user can dynamically edit the languages that can be added.

The pros of the above implementation is:
1) We do not need to create a new field everytime a new language support is to be added.
2) The model schema need not be altered whenever a new language has to be added

The cons are:
1) The JSON object might not be as human readable as compared to having multiple fields displayed seperately.
2) The JSON object might not perform well compared to multiple fields as the database has to serialize and deserialize the JSON object everytime.
