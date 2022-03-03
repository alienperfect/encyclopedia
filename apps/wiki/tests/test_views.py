from django.test import TestCase
from django.urls import reverse
from apps.accounts.models import User
from apps.wiki.models import Article, Category


class ArticleListViewTest(TestCase):
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('wiki:article-list'))
        self.assertTemplateUsed(response, 'article_list.html')


class ArticleDetailViewTest(TestCase):
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


class ArticleCreateViewTest(TestCase):
    def test_uses_correct_template(self):
        response = self.client.get(reverse('wiki:article-create'))
        self.assertTemplateUsed(response, 'article_create.html')


class ArticleEditViewTest(TestCase):
    def test_uses_correct_template(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        Article.objects.create(title='Bongo', editor=user)
        response = self.client.get(reverse('wiki:article-edit', kwargs={'title': 'Bongo'}))
        self.assertTemplateUsed(response, 'article_edit.html')


class ArticleHistoryListViewTest(TestCase):
    def test_view_uses_correct_template(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        Article.objects.create(title='Bongo', editor=user)
        response = self.client.get(reverse('wiki:article-history-list', kwargs={'title': 'Bongo'}))
        self.assertTemplateUsed(response, 'article_history_list.html')

    def test_view_displays_all_article_versions(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        article = Article.objects.create(title='Bongo', text='The first version', editor=user)
        article.text = 'The second version'
        article.save()
        expected_num = 2
        response = self.client.get(reverse('wiki:article-history-list', kwargs={'title': 'Bongo'}))
        num = response.context['history_list'].count()
        self.assertEqual(num, expected_num)


class ArticleHistoryDetailViewTest(TestCase):
    def test_view_uses_correct_template(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        Article.objects.create(title='Bongo', editor=user)
        response = self.client.get(reverse('wiki:article-history-detail', kwargs={'title': 'Bongo', 'version': 1}))
        self.assertTemplateUsed(response, 'article_history_detail.html')


class CategoryListViewTest(TestCase):
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('wiki:category-list'))
        self.assertTemplateUsed(response, 'category_list.html')


class CategoryDetailViewTest(TestCase):
    def test_view_uses_correct_template(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        Category.objects.create(title='Drums', editor=user)
        response = self.client.get(reverse('wiki:category-detail', kwargs={'title': 'Drums'}))
        self.assertTemplateUsed(response, 'category_detail.html')


class CategoryCreateViewTest(TestCase):
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('wiki:category-create'))
        self.assertTemplateUsed(response, 'category_create.html')


class CategoryEditViewTest(TestCase):
    def test_view_uses_correct_template(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        Category.objects.create(title='Drums', editor=user)
        response = self.client.get(reverse('wiki:category-edit', kwargs={'title': 'Drums'}))
        self.assertTemplateUsed(response, 'category_edit.html')


class CategoryHistoryListViewTest(TestCase):
    def test_view_uses_correct_template(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        Category.objects.create(title='Drums', editor=user)
        response = self.client.get(reverse('wiki:category-history-list', kwargs={'title': 'Drums'}))
        self.assertTemplateUsed(response, 'category_history_list.html')

    def test_view_displays_all_article_versions(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        category = Category.objects.create(title='Drums', text='The first version', editor=user)
        category.text = 'The second version'
        category.save()
        expected_num = 2
        response = self.client.get(reverse('wiki:category-history-list', kwargs={'title': 'Drums'}))
        num = response.context['history_list'].count()
        self.assertEqual(num, expected_num)


class CategoryHistoryDetailViewTest(TestCase):
    def test_view_uses_correct_template(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        Category.objects.create(title='Drums', editor=user)
        response = self.client.get(reverse('wiki:category-history-detail', kwargs={'title': 'Drums', 'version': 1}))
        self.assertTemplateUsed(response, 'category_history_detail.html')
