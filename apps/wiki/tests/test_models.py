from django.test import TestCase
from django.urls import reverse
from apps.accounts.models import User
from apps.wiki.models import Article


class ArticleModelTest(TestCase): 
    def test_object_name_is_title(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        Article.objects.create(title='Bongo', editor=user)
        article = Article.objects.get(id=1)
        expected_object_name = article.title
        self.assertEqual(str(article), expected_object_name)

    def test_get_absolute_url_is_detail_view(self):
        user = User.objects.create_user(username='alien', email='alien@email.com', password='')
        Article.objects.create(title='Bongo', editor=user)
        article = Article.objects.get(id=1)
        expected_url = reverse('wiki:article-detail', kwargs={'title': 'Bongo'})
        self.assertEqual(article.get_absolute_url(), expected_url)

    def test_save_on_create(self):
        User.objects.create_user(email='alien@email.com', username='alien', password='')
        self.client.login(username='alien', password='')
        post_dict = {'title': 'Cookie', 'text': 'Milk.'}
        expected = {'title': 'Cookie', 'text': 'Milk.', 'editor__username': 'alien', 'version': 1}
        response = self.client.post(reverse('wiki:article-create'), post_dict)
        article = Article.objects.filter(title='Cookie').values('title', 'text', 'editor__username', 'version')
        self.assertRedirects(response, expected_url='/', status_code=302)
        self.assertEqual(list(article), [expected])

    def test_save_on_edit(self):
        User.objects.create_user(email='alien@email.com', username='alien', password='')
        self.client.login(username='alien', password='')
        Article.objects.create(title='Cookie', text='Milk.', editor=User.objects.get(username='alien'))
        post_dict = {'text': 'Beer.', 'msg': 'edit'}
        expected = {'title': 'Cookie', 'text': 'Beer.', 'editor__username': 'alien', 'version': 2}
        response = self.client.post(reverse('wiki:article-edit', kwargs={'title': 'Cookie'}), post_dict)
        article = Article.objects.filter(title='Cookie').values('title', 'text', 'editor__username', 'version')
        self.assertRedirects(response, expected_url=reverse('wiki:article-detail', kwargs={'title': 'Cookie'}), status_code=302)
        self.assertEqual(list(article), [expected])
