from django.urls import path
from django.contrib.auth.views import LogoutView
from apps.accounts.views import SignUpView, LoginView, ProfileView, ProfileActivityView

app_name = 'accounts'
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/activity/', ProfileActivityView.as_view(), name='profile-activity'),
]
