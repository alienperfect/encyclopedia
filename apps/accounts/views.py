from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from apps.accounts.forms import CustomAuthenticationForm, SignUpForm
from apps.accounts.models import User
from apps.wiki.models import Article, History


class SignUpView(CreateView):
    model = User
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('wiki:article-list')

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


class ProfileActivityView(ListView):
    model = Article
    template_name = 'profile_activity.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['my_articles'] = History.objects.filter(editor=user, json_data__model='wiki.article')
        context['my_categories'] = History.objects.filter(editor=user, json_data__model='wiki.category')

        return context
