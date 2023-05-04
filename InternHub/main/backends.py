from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model


class InternHubBackend(BaseBackend):
    def authenticate(self, request, user_id=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(id=user_id)
        except user_model.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        else:
            return None

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
