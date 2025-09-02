from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class PhoneOrUsernameModelBackend(ModelBackend):
    """
    Custom authentication backend to allow users to authenticate using either
    their username or phone number.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(
                Q(username=username) | Q(phone=username)
            )
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None
