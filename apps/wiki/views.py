from datetime import datetime
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from apps.wiki.models import Article, History, Category
from apps.wiki.forms import ArticleCreateForm, ArticleEditForm, CategoryCreateForm, CategoryEditForm


class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'
    paginate_by = 20
    ordering = ['title']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = Article.objects.count()

        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = Article.objects.get(title=self.kwargs['title'])
        context['category_list'] = Category.objects.filter(category=instance)

        return context

    def get_object(self):
        return Article.objects.get(title=self.kwargs['title'])


class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleCreateForm
    template_name = 'article_create.html'
    success_url = reverse_lazy('wiki:article-list')

    def form_valid(self, form):
        form.instance.editor = self.request.user

        return super().form_valid(form)


class ArticleEditView(UpdateView):
    model = Article
    form_class = ArticleEditForm
    template_name = 'article_edit.html'

    def form_valid(self, form):
        form.instance.editor = self.request.user

        return super().form_valid(form)

    def get_object(self):
        return Article.objects.get(title=self.kwargs['title'])


class ArticleHistoryListView(ListView):
    model = History
    template_name = 'article_history_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.kwargs['title']
        context['title'] = title
        context['history_list'] = History.objects.filter(Q(json_data__model='wiki.article') & Q(json_data__fields__title=title))

        return context


class ArticleHistoryDetailView(DetailView):
    model = History
    template_name = 'article_history_detail.html'

    def get_object(self):
        title = self.kwargs['title']
        version = int(self.kwargs['version'])

        return History.objects.filter(
            Q(json_data__model='wiki.article')
            & Q(json_data__fields__title=title)
            & Q(json_data__fields__version=version)
            ).first()


class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    paginate_by = 20
    ordering = ['title']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = Category.objects.get(title=self.kwargs['title'])
        context['article_list'] = Article.objects.filter(category=instance)

        return context

    def get_object(self):
        return Category.objects.get(title=self.kwargs['title'])


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryCreateForm
    template_name = 'category_create.html'
    success_url = reverse_lazy('wiki:category-list')

    def form_valid(self, form):
        form.instance.editor = self.request.user

        return super().form_valid(form)


class CategoryEditView(UpdateView):
    model = Category
    form_class = CategoryEditForm
    template_name = 'category_edit.html'

    def form_valid(self, form):
        form.instance.editor = self.request.user

        return super().form_valid(form)

    def get_object(self):
        return Category.objects.get(title=self.kwargs['title'])


class CategoryHistoryListView(ListView):
    model = History
    template_name = 'category_history_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.kwargs['title']
        context['title'] = title
        context['history_list'] = History.objects.filter(Q(json_data__model='wiki.category') & Q(json_data__fields__title=title))

        return context


class CategoryHistoryDetailView(DetailView):
    model = History
    template_name = 'category_history_detail.html'

    def get_object(self):
        title = self.kwargs['title']
        version = int(self.kwargs['version'])

        return History.objects.filter(
            Q(json_data__model='wiki.category')
            & Q(json_data__fields__title=title)
            & Q(json_data__fields__version=version)
            ).first()
