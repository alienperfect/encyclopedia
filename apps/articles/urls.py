from django.urls import path
from apps.articles.views import CategoriesView, ArticlesView, ArticleDetailView, ArticlesHistoryView, ArticleHistoryDetailView, ArticleCreateView, ArticleEditView

app_name = 'articles'
urlpatterns = [
    path('', ArticlesView.as_view(), name='articles'),
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('create/', ArticleCreateView.as_view(), name='articles-create'),
    path('article/<title>/', ArticleDetailView.as_view(), name='articles-detail'),
    path('article/<title>/history/', ArticlesHistoryView.as_view(), name='articles-history'),
    path('article/<title>/history/version=<int:version>', ArticleHistoryDetailView.as_view(), name='articles-detail-history'),
    path('article/<title>/edit/', ArticleEditView.as_view(), name='articles-edit')
]
