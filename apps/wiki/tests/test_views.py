import pdb
from django.test import TestCase
from django.urls import reverse
from apps.accounts.models import User
from apps.wiki.models import Article, Category


class ArticleListViewTest(TestCase):
    def test_view_exists_at_url(self):
        response = self.client.get(reverse('wiki:article-list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('wiki:article-list'))
        self.assertTemplateUsed(response, 'article_list.html')

    def test_displays_all_articles(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        for article_id in range(25):
            Article.objects.create(title=f'Bongo {article_id}', editor=user)

        response = self.client.get(reverse('wiki:article-list') + '?page=2')
        self.assertEqual(len(response.context['article_list']), 5)


class ArticleDetailViewTest(TestCase):
    def test_view_exists_at_url(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        Article.objects.create(title='Bongo', editor=user)
        response = self.client.get(reverse('wiki:article-detail', kwargs={'title': 'Bongo'}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        Article.objects.create(title='Bongo', editor=user)
        response = self.client.get(reverse('wiki:article-detail', kwargs={'title': 'Bongo'}))
        self.assertTemplateUsed(response, 'article_detail.html')

    def test_view_displays_categories_related_to_article(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        category_1 = Category.objects.create(title='Drums', editor=user)
        category_2 = Category.objects.create(title='Sound', editor=user)
        article = Article.objects.create(title='Bongo', editor=user)
        article.category.add(category_1, category_2)
        response = self.client.get(reverse('wiki:article-detail', kwargs={'title': 'Bongo'}))
        category_list = list(response.context['category_list'].values('title'))
        expected_list = [{'title': 'Drums'}, {'title': 'Sound'}]
        self.assertEqual(category_list, expected_list)
