from django.db import models
from accounts.models import User


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
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.title
