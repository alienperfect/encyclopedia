from django.urls import path
from apps.wiki.views import ArticleListView, ArticleDetailView, ArticleCreateView, ArticleEditView, ArticleHistoryListView, ArticleHistoryDetailView, CategoryListView, CategoryDetailView, CategoryCreateView, CategoryEditView, CategoryHistoryListView, CategoryHistoryDetailView

app_name = 'wiki'
urlpatterns = [
    path('', ArticleListView.as_view(), name='article-list'),
    path('topic/new/', ArticleCreateView.as_view(), name='article-create'),
    path('topic/<str:title>/', ArticleDetailView.as_view(), name='article-detail'),
    path('topic/<str:title>/edit/', ArticleEditView.as_view(), name='article-edit'),
    path('topic/<str:title>/history/', ArticleHistoryListView.as_view(), name='article-history-list'),
    path('topic/<str:title>/history/<int:version>/', ArticleHistoryDetailView.as_view(), name='article-history-detail'),
    path('browse/', CategoryListView.as_view(), name='category-list'),
    path('browse/<str:title>/', CategoryDetailView.as_view(), name='category-detail'),
    path('create/category/', CategoryCreateView.as_view(), name='category-create'),
    path('browse/<str:title>/edit/', CategoryEditView.as_view(), name='category-edit'),
    path('browse/<str:title>/history/', CategoryHistoryListView.as_view(), name='category-history-list'),
    path('browse/<str:title>/history/<int:version>/', CategoryHistoryDetailView.as_view(), name='category-history-detail'),
]
