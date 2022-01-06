from django.http.response import HttpResponseRedirect
from django.views.generic import UpdateView, CreateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from .models import Article
from .forms import ArticleCreateForm, ArticleEditForm
from titles.models import Title


class ArticlesView(ListView):
    model = Article
    template_name = 'articles.html'
    paginate_by = 25
    ordering = ['title']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = Article.objects.count()

        return context


class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleCreateForm
    template_name = 'article_create.html'
    success_url = reverse_lazy('articles:articles')

    def form_valid(self, form):
        article = form.save(commit=False)
        article.created_by = self.request.user
        article.save()

        return super().form_valid(form)


class ArticleEditView(UpdateView):
    model = Article
    form_class = ArticleEditForm
    template_name = 'article_edit.html'

    def form_valid(self, form):
        article = Article.objects.get(pk=self.object.id)
        article.pk = None
        article.text = self.object.text
        article.created_by_id = self.request.user.id
        article.version = self.object.version + 1
        article.save()

        return HttpResponseRedirect(reverse('articles:articles'))

    def get_object(self):
        title = Title.objects.get(title=self.kwargs['title'])
        article = Article.objects.get(Q(title=title.pk) & Q(version=self.kwargs['version']))

        return article
