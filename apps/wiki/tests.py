from django.test import TestCase
from django.urls import reverse
from apps.accounts.models import User
from apps.wiki.models import Article


class ArticleTestCase(TestCase):
    def test_abstract_save_on_create(self):
        User.objects.create_user(email='alien@email.com', username='alien', password='')
        self.client.login(username='alien', password='')

        post_dict = {'title': 'Cookie', 'text': 'Milk.'}
        expected = {'title': 'Cookie', 'text': 'Milk.', 'editor__username': 'alien', 'version': 1}
        response = self.client.post(reverse('wiki:article-create'), post_dict)

        article = Article.objects.filter(title='Cookie').values('title', 'text', 'editor__username', 'version')

        self.assertRedirects(response, expected_url='/', status_code=302)
        self.assertEqual(list(article), [expected])

    def test_abstract_save_on_edit(self):
        User.objects.create_user(email='alien@email.com', username='alien', password='')
        self.client.login(username='alien', password='')

        Article.objects.create(title='Cookie', text='Milk.', editor=User.objects.get(username='alien'))
        post_dict = {'text': 'Beer.', 'msg': 'edit'}
        expected = {'title': 'Cookie', 'text': 'Beer.', 'editor__username': 'alien', 'version': 2}
        response = self.client.post(reverse('wiki:article-edit', kwargs={'title': 'Cookie'}), post_dict)

        article = Article.objects.filter(title='Cookie').values('title', 'text', 'editor__username', 'version')

        self.assertRedirects(response, expected_url=reverse('wiki:article-detail', kwargs={'title': 'Cookie'}), status_code=302)
        self.assertEqual(list(article), [expected])
