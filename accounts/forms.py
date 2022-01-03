from django import forms
from django.db.models import Q
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from .models import User


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )

    class Meta:
        model = User
        fields = ('email', 'username',)


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(label='Username or Email', widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        try:
            user = User.objects.get(Q(username__iexact=username)
                                          | Q(email__iexact=username))
            if not user.check_password(password):
                raise forms.ValidationError('Login or password is incorrect.')
        except User.DoesNotExist:
            raise forms.ValidationError('Login or password is incorrect.')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
