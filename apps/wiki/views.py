from datetime import datetime
from django.db.models import Q
from django.http.response import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from apps.wiki.models import Article, History, Category
from apps.wiki.forms import ArticleCreateForm, ArticleEditForm, CategoryCreateForm, CategoryEditForm


class ArticleListView(generic.ListView):
    model = Article
    template_name = 'article_list.html'
    paginate_by = 25
    ordering = ['title']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = Article.objects.count()

        return context


class ArticleDetailView(generic.DetailView):
    model = Article
    template_name = 'article_detail.html'

    def get_object(self):
        return Article.objects.get(title=self.kwargs['title'])


class ArticleCreateView(generic.CreateView):
    model = Article
    form_class = ArticleCreateForm
    template_name = 'article_create.html'
    success_url = reverse_lazy('wiki:article-list')

    def form_valid(self, form):
        form.instance.editor = self.request.user
        form.save()
        article_copy = History.objects.create(
            json_data={
                'type': self.model.__name__,
                'title': form.cleaned_data['title'],
                'text': form.cleaned_data['text'],
                'editor': self.request.user.username,
                'editor_id': self.request.user.id,
                'edited_on': datetime.utcnow().isoformat(),
                'version': 1,
                'msg': form.instance.msg,
                },
            content_object=form.instance
            )

        article_copy.save()

        return super().form_valid(form)


class ArticleEditView(generic.UpdateView):
    model = Article
    form_class = ArticleEditForm
    template_name = 'article_edit.html'

    def form_valid(self, form):
        form.instance.editor = self.request.user
        form.instance.edited_on = datetime.now()
        form.instance.version += 1
        form.save()

        article_copy = History.objects.create(
            json_data={
                'type': self.model.__name__,
                'title': form.instance.title,
                'text': form.cleaned_data['text'],
                'editor': self.request.user.username,
                'editor_id': self.request.user.id,
                'edited_on': datetime.utcnow().isoformat(),
                'version': form.instance.version,
                'msg': form.instance.msg,
                },
            content_object=form.instance
            )

        article_copy.save()

        return HttpResponseRedirect(reverse('wiki:article-detail', kwargs={'title': form.instance.title}))

    def get_object(self):
        return Article.objects.get(title=self.kwargs['title'])


class ArticleHistoryListView(generic.ListView):
    model = History
    template_name = 'history_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.kwargs['title']
        context['article_list'] = History.objects.filter(Q(json_data__type=Article.__name__) & Q(json_data__title=title)).order_by('-json_data__version')
        context['title'] = title

        return context


class ArticleHistoryDetailView(generic.DetailView):
    model = History
    template_name = 'history_detail.html'

    def get_object(self):
        return History.objects.filter(Q(json_data__type=Article.__name__) & Q(json_data__title=self.kwargs['title']) & Q(json_data__version=self.kwargs['version']))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = History.objects.filter(Q(json_data__title__icontains=self.kwargs['title']) & Q(json_data__version=int(self.kwargs['version'])))[0]

        return context


class CategoryListView(generic.ListView):
    model = Category
    template_name = 'category_list.html'
    paginate_by = 25
    ordering = ['title']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = 'category_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = Category.objects.get(title=self.kwargs['title'])
        context['article_list'] = Article.objects.filter(category=instance)

        return context

    def get_object(self):
        return Category.objects.get(title=self.kwargs['title'])


class CategoryCreateView(generic.CreateView):
    model = Category
    form_class = CategoryCreateForm
    template_name = 'category_create.html'
    success_url = reverse_lazy('wiki:category-list')

    def form_valid(self, form):
        form.instance.editor = self.request.user
        form.save()

        category_copy = History.objects.create(
            json_data={
                'type': self.model.__name__,
                'title': form.cleaned_data['title'],
                'text': form.cleaned_data['text'],
                'editor': self.request.user.username,
                'editor_id': self.request.user.id,
                'edited_on': datetime.utcnow().isoformat(),
                'version': 1,
                'msg': form.instance.msg,
                },
            content_object=form.instance
            )

        category_copy.save()

        return super().form_valid(form)


class CategoryEditView(generic.UpdateView):
    model = Category
    form_class = CategoryEditForm
    template_name = 'category_edit.html'

    def form_valid(self, form):
        form.instance.editor = self.request.user
        form.instance.edited_on = datetime.now()
        form.instance.version += 1
        form.save()

        category_copy = History.objects.create(
            json_data={
                'type': self.model.__name__,
                'title': form.instance.title,
                'text': form.cleaned_data['text'],
                'editor': self.request.user.username,
                'editor_id': self.request.user.id,
                'edited_on': datetime.utcnow().isoformat(),
                'version': form.instance.version,
                'msg': form.instance.msg,
                },
            content_object=form.instance
            )

        category_copy.save()

        return HttpResponseRedirect(reverse('wiki:category-detail', kwargs={'title': form.instance.title}))

    def get_object(self):
        return Category.objects.get(title=self.kwargs['title'])


class CategoryHistoryListView(generic.ListView):
    model = History
    template_name = 'category_history_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.kwargs['title']
        context['category_list'] = History.objects.filter(Q(json_data__type=Category.__name__) & Q(json_data__title=title)).order_by('-json_data__version')
        context['title'] = title

        return context


class CategoryHistoryDetailView(generic.DetailView):
    model = History
    template_name = 'category_history_detail.html'

    def get_object(self):
        return History.objects.filter(Q(json_data__type=Category.__name__) & Q(json_data__title=self.kwargs['title']) & Q(json_data__version=self.kwargs['version']))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = History.objects.filter(Q(json_data__type=Category.__name__) & Q(json_data__title=self.kwargs['title']) & Q(json_data__version=int(self.kwargs['version'])))[0]

        return context
