from django.urls import path
from .views import CategoriesView

app_name = 'categories'
urlpatterns = [
    path('', CategoriesView.as_view(), name='categories')
]
