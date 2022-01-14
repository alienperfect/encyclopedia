from django.contrib import admin
from apps.articles.models import Article, Category

admin.site.register(Article)
admin.site.register(Category)
