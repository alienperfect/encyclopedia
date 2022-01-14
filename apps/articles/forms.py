from django import forms
from django.core.exceptions import ObjectDoesNotExist
from apps.articles.models import Article, Category


class ArticleCreateForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(required=False, queryset=Category.objects.all())

    class Meta:
        model = Article
        fields = ['title', 'text', 'category']

    def clean_title(self):
        title = self.data['title']
        try:
            Article.objects.get(title=title)
            raise forms.ValidationError('Article with this title already exists.')
        except ObjectDoesNotExist:
            return title


class ArticleEditForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(required=False, queryset=Category.objects.all())

    class Meta:
        model = Article
        fields = ['text', 'category']

    def clean_text(self):
        pk = self.instance.pk
        text = self.cleaned_data['text']
        previous = Article.objects.get(pk=pk)

        if text == previous.text:
            raise forms.ValidationError('No changes detected.')

        return text
