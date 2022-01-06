from django.urls import path
from .views import ArticlesView, ArticleEditView

app_name = 'articles'
urlpatterns = [
    path('', ArticlesView.as_view(), name='articles'),
    path('edit/<title>/version=<int:pk>', ArticleEditView.as_view(), name='edit')
]
