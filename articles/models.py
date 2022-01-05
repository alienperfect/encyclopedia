from django.db import models
from django.conf import settings
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=254, unique=True)

    class Meta:
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=254)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, blank=True, null=True)
    
    def get_absolute_url(self):
        return reverse('articles:edit', kwargs={'title': self.title, 'pk': self.pk})

    def __str__(self):
        return self.title
