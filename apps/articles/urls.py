from django.urls import path
from apps.articles.views import TitlesView, TitleCreateView, CategoriesView, ArticlesView, ArticleDetailView, ArticlesHistoryView, ArticleHistoryDetailView, ArticleCreateView, ArticleEditView

app_name = 'articles'
urlpatterns = [
    path('', ArticlesView.as_view(), name='articles'),
    path('titles/', TitlesView.as_view(), name='titles'),
    path('titles/create/', TitleCreateView.as_view(), name='titles-create'),
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('<title>/', ArticleDetailView.as_view(), name='articles-detail'),
    path('<title>/history/', ArticlesHistoryView.as_view(), name='articles-history'),
    path('<title>/history/version=<int:version>', ArticleHistoryDetailView.as_view(), name='articles-detail-history'),
    path('create/', ArticleCreateView.as_view(), name='articles-create'),
    path('<title>/edit/', ArticleEditView.as_view(), name='articles-edit')
]
