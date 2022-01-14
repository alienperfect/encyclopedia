from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings
from django.urls import reverse


class Article(models.Model):
    title = models.CharField(max_length=256, unique=True)
    text = models.TextField(blank=True)
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    edited_on = models.DateTimeField(auto_now_add=True)
    version = models.IntegerField(default=1)
    category = models.ManyToManyField('Category')

    def __str__(self):
        return self.title

    def get_absolute_detail(self):
        return reverse('articles:article-detail', kwargs={'title': self.title})

    def get_absolute_edit(self):
        return reverse('articles:article-edit', kwargs={'title': self.title})

    def get_absolute_history(self):
        return reverse('articles:history-list', kwargs={'title': self.title})

    def get_absolute_history_detail(self):
        return reverse('articles:article-history-detail', kwargs={'title': self.title, 'version': self.version})


class ArticleOld(models.Model):
    content = models.JSONField()
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    edited_on = models.DateTimeField(auto_now_add=True)
    version = models.IntegerField(default=1)

    def __str__(self):
        return self.content['title']

    def get_absolute_url(self):
        return reverse('articles:history-detail', kwargs={'title': self.content['title'], 'version': self.version})
    
    def get_absolute_edit(self):
        return reverse('articles:article-edit', kwargs={'title': self.content['title']})
    
    def get_absolute_history(self):
        return reverse('articles:history-list', kwargs={'title': self.content['title']})


class Category(models.Model):
    name = models.CharField(max_length=256, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
