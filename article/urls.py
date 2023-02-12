from .views import display_title_table,ArticleModView
from django.urls.conf import path
urlpatterns = [
    path('',display_title_table,name='display_title_table'),
    path('article/',ArticleModView.as_view()),
    path('article/<int:id>',ArticleModView.as_view())
]
