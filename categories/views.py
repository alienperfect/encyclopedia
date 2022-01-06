from django.views.generic.list import ListView
from django.urls import reverse_lazy
from .models import Category


class CategoriesView(ListView):
    model = Category
    template_name = 'categories.html'
    paginate_by = 25
    extra_context = {'count': Category.objects.count()}
