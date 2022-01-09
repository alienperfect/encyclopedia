from django.db import models
from django.conf import settings
from django.urls import reverse


class Title(models.Model):
    title = models.CharField(unique=True, max_length=256)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=256, unique=True)

    class Meta:
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.ForeignKey('Title', on_delete=models.CASCADE, null=True)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    category = models.ManyToManyField(Category, blank=True)
    version = models.IntegerField(default=1)

    def get_absolute_url_edit(self):
        return reverse('articles:articles-edit', kwargs={'title': self.title})

    def get_absolute_url_detail(self):
        return reverse('articles:articles-detail', kwargs={'title': self.title})

    def get_absolute_url_history(self):
        return reverse('articles:articles-history', kwargs={'title': self.title})

    def get_absolute_url_history_detail(self):
        return reverse('articles:articles-detail-history', kwargs={'title': self.title, 'version': self.version})

    def __str__(self):
        return self.title.title
