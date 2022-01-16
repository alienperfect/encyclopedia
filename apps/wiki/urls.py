from django.urls import path
from apps.wiki.views import ArticleListView, ArticleDetailView, ArticleCreateView, ArticleEditView, ArticleHistoryListView, ArticleHistoryDetailView, CategoryListView, CategoryDetailView, CategoryCreateView, CategoryEditView, CategoryHistoryListView, CategoryHistoryDetailView

app_name = 'wiki'
urlpatterns = [
    path('', ArticleListView.as_view(), name='article-list'),
    path('topic/<title>/', ArticleDetailView.as_view(), name='article-detail'),
    path('create/article/', ArticleCreateView.as_view(), name='article-create'),
    path('topic/<title>?action=edit', ArticleEditView.as_view(), name='article-edit'),
    path('topic/<title>?action=history', ArticleHistoryListView.as_view(), name='article-history-list'),
    path('topic/<title>?action=history&version=<version>', ArticleHistoryDetailView.as_view(), name='article-history-detail'),
    path('browse/', CategoryListView.as_view(), name='category-list'),
    path('browse/<title>/', CategoryDetailView.as_view(), name='category-detail'),
    path('create/category/', CategoryCreateView.as_view(), name='category-create'),
    path('browse/<title>?action=edit', CategoryEditView.as_view(), name='category-edit'),
    path('browse/<title>?action=history', CategoryHistoryListView.as_view(), name='category-history-list'),
    path('browse/<title>?action=history&version=<version>', CategoryHistoryDetailView.as_view(), name='category-history-detail'),
]
