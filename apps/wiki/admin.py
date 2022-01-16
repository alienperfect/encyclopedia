from django.contrib import admin
from apps.wiki.models import Article, Category

admin.site.register(Article)
admin.site.register(Category)
