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


class ArticleCreateViewTest(TestCase):
    def test_view_exists_at_url(self):
        response = self.client.get(reverse('wiki:article-create'))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse('wiki:article-create'))
        self.assertTemplateUsed(response, 'article_create.html')


class ArticleEditViewTest(TestCase):
    def test_view_exists_at_url(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        Article.objects.create(title='Bongo', editor=user)
        response = self.client.get(reverse('wiki:article-edit', kwargs={'title': 'Bongo'}))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        Article.objects.create(title='Bongo', editor=user)
        response = self.client.get(reverse('wiki:article-edit', kwargs={'title': 'Bongo'}))
        self.assertTemplateUsed(response, 'article_edit.html')


class ArticleHistoryListViewTest(TestCase):
    def test_view_exists_at_url(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        Article.objects.create(title='Bongo', editor=user)
        response = self.client.get(reverse('wiki:article-history-list', kwargs={'title': 'Bongo'}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        Article.objects.create(title='Bongo', editor=user)
        response = self.client.get(reverse('wiki:article-history-list', kwargs={'title': 'Bongo'}))
        self.assertTemplateUsed(response, 'article_history_list.html')


class ArticleHistoryDetailViewTest(TestCase):
    def test_view_exists_at_url(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        Article.objects.create(title='Bongo', editor=user)
        response = self.client.get(reverse('wiki:article-history-detail', kwargs={'title': 'Bongo', 'version': 1}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        Article.objects.create(title='Bongo', editor=user)
        response = self.client.get(reverse('wiki:article-history-detail', kwargs={'title': 'Bongo', 'version': 1}))
        self.assertTemplateUsed(response, 'article_history_detail.html')


class CategoryListViewTest(TestCase):
    def test_view_exists_at_url(self):
        response = self.client.get(reverse('wiki:category-list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('wiki:category-list'))
        self.assertTemplateUsed(response, 'category_list.html')

    def test_displays_all_categories(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        for category_id in range(25):
            Category.objects.create(title=f'Drums {category_id}', editor=user)

        response = self.client.get(reverse('wiki:category-list') + '?page=2')
        self.assertEqual(len(response.context['category_list']), 5)


class CategoryDetailViewTest(TestCase):
    def test_view_exists_at_url(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        Category.objects.create(title='Drums', editor=user)
        response = self.client.get(reverse('wiki:category-detail', kwargs={'title': 'Drums'}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        Category.objects.create(title='Drums', editor=user)
        response = self.client.get(reverse('wiki:category-detail', kwargs={'title': 'Drums'}))
        self.assertTemplateUsed(response, 'category_detail.html')


class CategoryCreateViewTest(TestCase):
    def test_view_exists_at_url(self):
        response = self.client.get(reverse('wiki:category-create'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('wiki:category-create'))
        self.assertTemplateUsed(response, 'category_create.html')


class CategoryEditViewTest(TestCase):
    def test_view_exists_at_url(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        Category.objects.create(title='Drums', editor=user)
        response = self.client.get(reverse('wiki:category-edit', kwargs={'title': 'Drums'}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        Category.objects.create(title='Drums', editor=user)
        response = self.client.get(reverse('wiki:category-edit', kwargs={'title': 'Drums'}))
        self.assertTemplateUsed(response, 'category_edit.html')


class CategoryHistoryListViewTest(TestCase):
    def test_view_exists_at_url(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        Category.objects.create(title='Drums', editor=user)
        response = self.client.get(reverse('wiki:category-history-list', kwargs={'title': 'Drums'}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        Category.objects.create(title='Drums', editor=user)
        response = self.client.get(reverse('wiki:category-history-list', kwargs={'title': 'Drums'}))
        self.assertTemplateUsed(response, 'category_history_list.html')


class CategoryHistoryDetailViewTest(TestCase):
    def test_view_exists_at_url(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        Category.objects.create(title='Drums', editor=user)
        response = self.client.get(reverse('wiki:category-history-detail', kwargs={'title': 'Drums', 'version': 1}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        Category.objects.create(title='Drums', editor=user)
        response = self.client.get(reverse('wiki:category-history-detail', kwargs={'title': 'Drums', 'version': 1}))
        self.assertTemplateUsed(response, 'category_history_detail.html')
