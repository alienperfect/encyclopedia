import pdb
from django.test import TestCase
from django.urls import reverse
from apps.accounts.models import User
from apps.wiki.forms import ArticleCreateForm, ArticleEditForm, CategoryCreateForm, CategoryEditForm
from apps.wiki.models import Article, Category


class ArticleCreateFormTest(TestCase):
    def test_title_label(self):
        form = ArticleCreateForm()
        self.assertTrue(form.fields['title'].label is None or form.fields['title'].label == 'Title')

    def test_text_label(self):
        form = ArticleCreateForm()
        self.assertTrue(form.fields['text'].label is None or form.fields['text'].label == 'Text')

    def test_category_label(self):
        form = ArticleCreateForm()
        self.assertTrue(form.fields['category'].label is None or form.fields['category'].label == 'Category')

    def test_no_title_duplicates(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        Article.objects.create(title='Bongo', editor=user)
        form = ArticleCreateForm(data={'title': 'Bongo'})
        self.assertFalse(form.is_valid())


class ArticleEditFormTest(TestCase):
    def test_text_label(self):
        form = ArticleEditForm()
        self.assertTrue(form.fields['text'].label is None or form.fields['text'].label == 'Text')

    def test_category_label(self):
        form = ArticleEditForm()
        self.assertTrue(form.fields['category'].label is None or form.fields['category'].label == 'Category')

    def test_msg_label(self):
        form = ArticleEditForm()
        self.assertTrue(form.fields['msg'].label is None or form.fields['msg'].label == 'Msg')

    def test_no_text_duplicates(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        article = Article.objects.create(title='Bongo', editor=user)
        form = ArticleEditForm({'msg': 'something'}, instance=article)
        self.assertFalse(form.is_valid())


class CategoryCreateFormTest(TestCase):
    def test_title_label(self):
        form = CategoryCreateForm()
        self.assertTrue(form.fields['title'].label is None or form.fields['title'].label == 'Title')

    def test_text_label(self):
        form = CategoryCreateForm()
        self.assertTrue(form.fields['text'].label is None or form.fields['text'].label == 'Text')

    def test_no_title_duplicates(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        category = Category.objects.create(title='Drums', editor=user)
        form = CategoryCreateForm({'title': 'Drums'}, instance=category)
        self.assertFalse(form.is_valid())


class CategoryEditFormTest(TestCase):
    def test_text_label(self):
        form = CategoryEditForm()
        self.assertTrue(form.fields['text'].label is None or form.fields['text'].label == 'Text')

    def test_msg_label(self):
        form = CategoryEditForm()
        self.assertTrue(form.fields['msg'].label is None or form.fields['msg'].label == 'Msg')

    def test_no_text_duplicates(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        category = Category.objects.create(title='Drums', editor=user)
        form = CategoryEditForm({'msg': 'something'}, instance=category)
        self.assertFalse(form.is_valid())
