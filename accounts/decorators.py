from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def role_required(*roles):
    """
    Decorator for views that checks if the user has one of the allowed roles.
    """
    def check_role(user):
        if user.is_authenticated and (user.role in roles or user.is_superuser):
            return True
        raise PermissionDenied
    return user_passes_test(check_role)
