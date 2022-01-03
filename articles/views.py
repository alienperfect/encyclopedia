from django.views.generic.list import ListView
from .models import Article


class ArticlesView(ListView):
    model = Article
    template_name = 'articles.html'
    paginate_by = 25
