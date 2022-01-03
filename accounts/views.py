from django.shortcuts import render
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm


class LoginView(LoginView):
    form_class = CustomAuthenticationForm
    authentication_form = CustomAuthenticationForm
    template_name = 'login.html'
    redirect_field_name = 'next'
    redirect_authenticated_user = True
