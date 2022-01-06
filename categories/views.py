from django.views.generic.list import ListView
from django.urls import reverse_lazy
from .models import Category


class CategoriesView(ListView):
    model = Category
    template_name = 'categories.html'
    paginate_by = 25
    ordering = ['name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = Category.objects.count()

        return context
