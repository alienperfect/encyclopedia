from django import forms
from django.urls import reverse_lazy
from apps.wiki.models import Article, Category


class ArticleCreateForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(required=False, queryset=Category.objects.all())

    class Meta:
        model = Article
        fields = ['title', 'text', 'category']

    def clean_title(self):
        title = self.data['title']
        if Article.objects.filter(title=title).exists():
            raise forms.ValidationError('Article with this title already exists.')

        return title


class ArticleEditForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(required=False, queryset=Category.objects.all())
    msg = forms.CharField(max_length=256, required=True)

    class Meta:
        model = Article
        fields = ['text', 'category', 'msg']

    def clean_text(self):
        pk = self.instance.pk
        text = self.cleaned_data['text']
        previous = Article.objects.get(pk=pk)

        if text == previous.text:
            raise forms.ValidationError('No changes detected.')

        return text


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'text']

    def clean_title(self):
        title = self.data['title']
        if Category.objects.filter(title=title).exists():
            raise forms.ValidationError('Category with this name already exists.')

        return title


class CategoryEditForm(forms.ModelForm):
    msg = forms.CharField(max_length=256, required=True)

    class Meta:
        model = Category
        fields = ['text', 'msg']

    def clean_text(self):
        pk = self.instance.pk
        text = self.cleaned_data['text']
        previous = Category.objects.get(pk=pk)

        if text == previous.text:
            raise forms.ValidationError('No changes detected.')

        return text
