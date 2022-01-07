from django.http.response import HttpResponseRedirect
from django.views.generic import UpdateView, CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from apps.articles.models import Title, Article, Category
from apps.articles.forms import TitleCreateForm, ArticleCreateForm, ArticleEditForm


class TitleCreateView(CreateView):
    model = Title
    form_class = TitleCreateForm
    template_name = 'title_create.html'
    success_url = reverse_lazy('titles:titles')


class TitlesView(ListView):
    model = Title
    template_name = 'titles.html'
    paginate_by = 25
    ordering = ['title']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = self.model.objects.count()

        return context


class CategoriesView(ListView):
    model = Category
    template_name = 'categories.html'
    paginate_by = 25
    ordering = ['name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = Category.objects.count()

        return context


class ArticlesView(ListView):
    model = Article
    template_name = 'articles.html'
    paginate_by = 25
    ordering = ['title']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = Title.objects.count()

        title = Title.objects.all()

        articles = []
        for num in range(len(title)):
            article = Article.objects.filter(title=title[num].pk).last()
            if article != None:
                articles.append(article)

        context['articles_unique'] = articles

        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.kwargs['title']

        return context

    def get_object(self):
        title = Title.objects.filter(title=self.kwargs['title']).first()

        if title.exists():
            article = Article.objects.filter(title=title.pk).latest('version')

        return article


class ArticlesHistoryView(ListView):
    model = Article
    template_name = 'articles_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = Title.objects.get(title=self.kwargs['title'])
        context['title'] = self.kwargs['title']
        context['articles_all'] = Article.objects.filter(title=title.pk)

        return context


class ArticleHistoryDetailView(DetailView):
    model = Article
    template_name = 'article_history_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.kwargs['title']

        return context

    def get_object(self):
        title = Title.objects.get(title=self.kwargs['title'])
        article = Article.objects.get(Q(title=title.pk) & Q(version=self.kwargs['version']))

        return article


class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleCreateForm
    template_name = 'article_create.html'
    success_url = reverse_lazy('articles:articles')

    def form_valid(self, form):
        article = form.save()
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
        article = Article.objects.filter(Q(title=title.pk)).last()

        return article
