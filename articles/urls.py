from django.urls import path
from .views import ArticlesView

app_name = 'articles'
urlpatterns = [
    path('', ArticlesView.as_view(), name='articles'),
]
