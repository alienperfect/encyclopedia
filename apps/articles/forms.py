from django import forms
from django.db.utils import IntegrityError
from apps.articles.models import Title, Category, Article


class TitleCreateForm(forms.ModelForm):

    class Meta:
        model = Title
        fields = '__all__'


class ArticleCreateForm(forms.ModelForm):
    title = forms.CharField(max_length=256)
    category = forms.ModelMultipleChoiceField(required=False, queryset=Category.objects.all())

    def clean_title(self):
        title = self.cleaned_data['title']
        try:
            return Title.objects.create(title=title)
        except IntegrityError:
            raise forms.ValidationError('Article with this title already exists.')

    class Meta:
        model = Article
        fields = ['title', 'text', 'category']


class ArticleEditForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(required=False, queryset=Category.objects.all())

    def clean_text(self):
        pk = self.instance.pk
        text = self.cleaned_data['text']
        previous = Article.objects.get(pk=pk)

        if text == previous.text:
            raise forms.ValidationError('No changes detected.')

        return text

    class Meta:
        model = Article
        fields = ['text', 'category']
