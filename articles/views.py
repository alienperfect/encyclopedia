from django.views.generic import UpdateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from .models import Article, Category
from .forms import ArticleEditForm


class ArticlesView(ListView):
    model = Article
    template_name = 'articles.html'
    paginate_by = 25
    extra_context = {'count': Article.objects.count()}


class ArticleEditView(UpdateView):
    model = Article
    form_class = ArticleEditForm
    template_name = 'article_edit.html'
    success_url = reverse_lazy('articles:articles')

    def form_valid(self, form):
        copy = Article.objects.get(pk=self.object.id)
        copy.pk = None
        copy.text = self.object.text
        copy.created_by_id = self.request.user.id
        copy.save()

        category_set = Category.objects.all()
        for category in category_set.iterator():
            self.object.category.set(category.id)

        return super().form_valid(form)
