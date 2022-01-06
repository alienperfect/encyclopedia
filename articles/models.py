from django.db import models
from django.conf import settings
from django.urls import reverse
from categories.models import Category


class Article(models.Model):
    title = models.CharField(max_length=254)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    category = models.ManyToManyField(Category)

    def get_absolute_url(self):
        return reverse('articles:edit', kwargs={'title': self.title, 'pk': self.pk})

    def __str__(self):
        return self.title
