from django.urls import path
from .views import ArticlesView, ArticlesEditView

app_name = 'articles'
urlpatterns = [
    path('', ArticlesView.as_view(), name='articles'),
    path('edit/<title>/version=<int:pk>', ArticlesEditView.as_view(), name='edit')
]
