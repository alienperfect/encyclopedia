from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from apps.accounts.models import User


class AuthenticationBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        username = kwargs['username'].lower()
        password = kwargs['password']
        try:
            user = User.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            pass
