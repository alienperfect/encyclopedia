from django.views.generic import CreateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from .models import Title
from .forms import TitleCreateForm


class TitleCreateView(CreateView):
    model = Title
    form_class = TitleCreateForm
    template_name = 'title_create.html'
    success_url = reverse_lazy('titles:titles')


class TitleView(ListView):
    model = Title
    template_name = 'titles.html'
    paginate_by = 25
    ordering = ['title']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = Title.objects.count()

        return context
