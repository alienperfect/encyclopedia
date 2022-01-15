from datetime import datetime
from django.db.models import Q
from django.http.response import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from apps.articles.models import Article, History, Category
from apps.articles.forms import ArticleCreateForm, ArticleEditForm


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
    success_url = reverse_lazy('articles:article-list')

    def form_valid(self, form):
        form.instance.editor = self.request.user
        form.save()

        article_copy = History.objects.create(
            json_data={
                'title': form.cleaned_data['title'],
                'text': form.cleaned_data['text'],
                'editor': self.request.user.username,
                'editor_id': self.request.user.id,
                'edited_on': datetime.utcnow().isoformat(),
                'version': 1,
                'msg': form.instance.msg
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
                'title': form.instance.title,
                'text': form.cleaned_data['text'],
                'editor': self.request.user.username,
                'editor_id': self.request.user.id,
                'edited_on': datetime.utcnow().isoformat(),
                'version': form.instance.version,
                'msg': form.instance.msg
                },
            content_object=form.instance
            )

        article_copy.save()

        return HttpResponseRedirect(reverse('articles:article-detail', kwargs={'title': form.instance.title}))

    def get_object(self):
        return Article.objects.get(title=self.kwargs['title'])


class HistoryListView(generic.ListView):
    model = History
    template_name = 'history_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.kwargs['title']
        context['article_list'] = History.objects.filter(json_data__icontains=title).order_by('-json_data__version')
        context['title'] = title

        return context


class HistoryDetailView(generic.DetailView):
    model = History
    template_name = 'history_detail.html'

    def get_object(self):
        return History.objects.filter(Q(json_data__title=self.kwargs['title']) & Q(json_data__version=self.kwargs['version']))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = History.objects.filter(Q(json_data__title__icontains=self.kwargs['title']) & Q(json_data__version=int(self.kwargs['version'])))[0]

        return context


class CategoryListView(generic.ListView):
    model = Category
    template_name = 'categories.html'
    paginate_by = 25
    ordering = ['name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = Category.objects.count()

        return context
