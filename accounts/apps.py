"""
Accounts App Configuration.
Registers the accounts app with Django and sets its display name.
"""
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Configuration class for the accounts application."""
    # Use BigAutoField as the default primary key type
    default_auto_field = 'django.db.models.BigAutoField'
    # The Python path to the application
    name = 'accounts'
    # Human-readable name displayed in Django admin
    verbose_name = 'User Accounts'
