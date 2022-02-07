import pdb
from django.test import TestCase
from apps.accounts.models import User
from apps.wiki.forms import ArticleCreateForm, ArticleEditForm
from apps.wiki.models import Article


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
