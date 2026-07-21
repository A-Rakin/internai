"""
============================================================
Accounts Decorators - Role-Based Access Control
============================================================
Custom decorators for enforcing role-based permissions
and redirecting authenticated users.
============================================================
"""

from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from functools import wraps
from django.shortcuts import redirect


def role_required(*roles):
    """
    Decorator for views that checks if the user has one of the allowed roles.
    Raises PermissionDenied (403) if the user doesn't have the required role.
    """
    def check_role(user):
        if user.is_authenticated and (user.role in roles or user.is_superuser):
            return True
        raise PermissionDenied
    return user_passes_test(check_role)


def redirect_authenticated(view_func):
    """
    Decorator that redirects already-authenticated users to their dashboard.
    Used on login and registration pages.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(request.user.get_dashboard_url())
        return view_func(request, *args, **kwargs)
    return wrapper
