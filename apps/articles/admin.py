from django.contrib import admin
from apps.articles.models import Title, Category, Article

admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Article)
