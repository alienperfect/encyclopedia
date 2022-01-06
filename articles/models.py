from django.db import models
from django.conf import settings
from django.urls import reverse
from categories.models import Category
from titles.models import Title


class Article(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, null=True)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    category = models.ManyToManyField(Category)
    version = models.IntegerField(default=1)

    def get_absolute_url(self):
        return reverse('articles:edit', kwargs={'title': self.title, 'version': self.version})
