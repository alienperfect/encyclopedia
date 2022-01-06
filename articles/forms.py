from django import forms
from django.db.utils import IntegrityError
from django.forms import ModelForm
from .models import Article
from titles.models import Title
from categories.models import Category


class ArticleCreateForm(ModelForm):
    title = forms.CharField(max_length=256)
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all())

    def clean_title(self):
        title = self.cleaned_data['title']
        try:
            return Title.objects.create(title=title)
        except IntegrityError:
            raise forms.ValidationError("Article with this title already exists.")


    class Meta:
        model = Article
        fields = ['title', 'text', 'category']


class ArticleEditForm(ModelForm):
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Article
        fields = ['text', 'category']
