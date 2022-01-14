from django.urls import path
from apps.articles.views import ArticleListView, ArticleDetailView, ArticleCreateView, ArticleEditView, HistoryListView, HistoryDetailView, CategoryListView

app_name = 'articles'
urlpatterns = [
    path('', ArticleListView.as_view(), name='article-list'),
    path('topic/<title>/', ArticleDetailView.as_view(), name='article-detail'),
    path('create/', ArticleCreateView.as_view(), name='articles-create'),
    path('topic/<title>?action=edit', ArticleEditView.as_view(), name='article-edit'),
    path('topic/<title>?action=history', HistoryListView.as_view(), name='history-list'),
    path('topic/<title>?action=history&version=<version>', HistoryDetailView.as_view(), name='history-detail'),
    path('browse/', CategoryListView.as_view(), name='categories')
]
