from django import forms
from .models import Title


class TitleCreateForm(forms.ModelForm):

    class Meta:
        model = Title
        fields = '__all__'
