from django.views.generic.list import ListView
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .models import Article
from .forms import ArticleEditForm


class ArticlesView(ListView):
    model = Article
    template_name = 'articles.html'
    paginate_by = 25


class ArticlesEditView(UpdateView):
    model = Article
    form_class = ArticleEditForm
    template_name = 'articles_edit.html'
    success_url = reverse_lazy('articles:articles')

    def form_valid(self, form):
        copy = Article.objects.get(pk=self.get_object().id)
        copy.pk = None
        copy.save()

        self.object = form.save()
        return super().form_valid(form)
