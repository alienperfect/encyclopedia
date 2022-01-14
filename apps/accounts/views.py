from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from apps.accounts.forms import CustomAuthenticationForm, SignUpForm
from apps.accounts.models import User
from apps.articles.models import Article


class SignUpView(CreateView):
    model = User
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('articles:article-list')

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return HttpResponseRedirect(self.get_success_url())


class LoginView(LoginView):
    form_class = CustomAuthenticationForm
    authentication_form = CustomAuthenticationForm
    template_name = 'login.html'
    redirect_field_name = 'next'
    redirect_authenticated_user = True


class ProfileView(ListView):
    model = Article
    template_name = 'profile.html'
