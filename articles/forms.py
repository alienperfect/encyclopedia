from django import forms
from django.forms import ModelForm
from .models import Article, Category


class ArticleEditForm(ModelForm):
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all())
    class Meta:
        model = Article
        fields = ['text', 'category']
