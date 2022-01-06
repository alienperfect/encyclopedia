from django.urls import path
from .views import ArticlesView, ArticleCreateView, ArticleEditView

app_name = 'articles'
urlpatterns = [
    path('', ArticlesView.as_view(), name='articles'),
    path('create/', ArticleCreateView.as_view(), name='create'),
    path('edit/<title>/version=<int:version>', ArticleEditView.as_view(), name='edit')
]
