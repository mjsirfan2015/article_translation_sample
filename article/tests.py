from django.test import TestCase
from django.test import RequestFactory, TestCase
from django.urls import reverse
from .models import Article
from .views import display_title_table, ArticleModView

class ArticleViewsTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.article1 = Article.objects.create(title={'en': 'Test Title 1', 'fr': 'Test Title 1 en français'})
        self.article2 = Article.objects.create(title={'en': 'Test Title 2', 'fr': 'Test Title 2 en français'})

    def test_display_title_table(self):
        """
            A test written for display_title_table view. calls the view and checks if status code is 200 and if the length
            of context data is equal to that of
            the no of all articles.
        """
        request = self.factory.get(reverse('display_title_table'))
        response = display_title_table(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data['articles']), 2)

    def test_article_mod_view_get(self):
        """
            A test written for GET in article_mod_view view. calls the view and checks if 200 and compares id and article id in context data
        """
        request = self.factory.get(reverse('mod_article', args=[self.article1.id]))
        response = ArticleModView.as_view()(request, id=self.article1.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['id'], self.article1.id)
        self.assertEqual(response.context_data['article'].id, self.article1.id)

        request = self.factory.get(reverse('mod_article', args=[1000]))
        response = ArticleModView.as_view()(request, id=1000)
        self.assertEqual(response.status_code, 404)

    def test_article_mod_view_post_create(self):
        """
            check for article_mod_view POST in object creation. checks if redirection occurs and new data is created
        """
        data = {
            'en': 'Test Title 3',
            'fr': 'Test Title 3 en français',
        }
        request = self.factory.post(reverse('mod_article'), data=data)
        response = ArticleModView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Article.objects.count(), 3)

    def test_article_mod_view_post_update(self):
        """
            check for article_mod_view POST in object updation. checks if redirection occurs and updated data compared
        """
        data = {
            'en': 'Updated Test Title 1',
            'fr': 'Updated Test Title 1 en français',
        }
        request = self.factory.post(reverse('mod_article', args=[self.article1.id]), data=data)
        response = ArticleModView.as_view()(request, id=self.article1.id)
        self.assertEqual(response.status_code, 302)
        article = Article.objects.get(id=self.article1.id)
        self.assertEqual(article.title, data)

