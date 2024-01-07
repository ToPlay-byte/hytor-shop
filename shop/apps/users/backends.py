from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ObjectDoesNotExist

from .models import CustomUser


class Authentication(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None or password is None:
            email = request.POST['username']
            password = request.POST['password']
        try:
            user = CustomUser.objects.get(email=email)
        except ObjectDoesNotExist:
            return None
        else:
            check = user.check_password(password)
            if check and self.user_can_authenticate(user):
                return user
            return None
