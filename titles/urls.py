from django.urls import path
from .views import TitleView, TitleCreateView

app_name = 'titles'
urlpatterns = [
    path('', TitleView.as_view(), name='titles'),
    path('create/', TitleCreateView.as_view(), name='create')
]
