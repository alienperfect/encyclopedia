import pdb
from django.forms import ValidationError
from django.test import TestCase
from apps.accounts.models import User
from apps.wiki.forms import ArticleCreateForm, ArticleEditForm, CategoryCreateForm, CategoryEditForm
from apps.wiki.models import Article, Category


class ArticleCreateFormTest(TestCase):
    def test_try_to_create_existing_title(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        Article.objects.create(title='Bongo', editor=user)
        form = ArticleCreateForm(data={'title': 'Bongo'})
        self.assertRaises(ValidationError, form.clean_title)

    def test_try_to_create_non_existing_title(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        Article.objects.create(title='Bongo', editor=user)
        form = ArticleCreateForm(data={'title': 'Not bongo'})
        self.assertTrue(form.is_valid())


class ArticleEditFormTest(TestCase):
    def test_try_to_save_the_same_text(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        article = Article.objects.create(title='Bongo', text='1', editor=user)
        form = ArticleEditForm({'text': '1', 'msg': 'Nothing has changed'}, instance=article)
        self.assertFalse(form.is_valid())

    def test_try_to_save_text(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        article = Article.objects.create(title='Bongo', editor=user)
        form = ArticleEditForm({'text': '1', 'msg': '1'}, instance=article)
        self.assertTrue(form.is_valid())


class CategoryCreateFormTest(TestCase):
    def test_try_to_create_existing_title(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        Category.objects.create(title='Drums', editor=user)
        form = CategoryCreateForm(data={'title': 'Drums'})
        self.assertRaises(ValidationError, form.clean_title)

    def test_try_to_create_non_existing_title(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        Category.objects.create(title='Drums', editor=user)
        form = CategoryCreateForm(data={'title': 'Not drums'})
        self.assertTrue(form.is_valid())


class CategoryEditFormTest(TestCase):
    def test_try_to_save_the_same_text(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        category = Category.objects.create(title='Drums', text='1', editor=user)
        form = CategoryEditForm({'text': '1', 'msg': 'Nothing has changed'}, instance=category)
        self.assertFalse(form.is_valid())

    def test_try_to_save_text(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        category = Category.objects.create(title='Drums', editor=user)
        form = CategoryEditForm({'text': '1', 'msg': '1'}, instance=category)
        self.assertTrue(form.is_valid())
