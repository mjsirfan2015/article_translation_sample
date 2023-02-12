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