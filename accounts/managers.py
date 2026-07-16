"""
============================================================
Accounts - Custom User Manager
============================================================
Handles creation of regular users and superusers with email
as the primary authentication field instead of username.
============================================================
"""

# Import Django's base user manager
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user manager that uses email as the unique identifier
    for authentication instead of the default username field.
    """

    def create_user(self, email, username, password=None, **extra_fields):
        """
        Create and return a regular user with the given email and password.
        
        Args:
            email: User's email address (required, used for login)
            username: User's username (required, must be unique)
            password: User's password (will be hashed before storing)
            **extra_fields: Additional fields like first_name, last_name, role
        
        Returns:
            CustomUser: The newly created user instance
        
        Raises:
            ValueError: If email is not provided
        """
        # Validate that email is provided
        if not email:
            raise ValueError('Users must have an email address')

        # Normalize the email address (lowercase the domain part)
        email = self.normalize_email(email)

        # Create the user model instance (not yet saved to database)
        user = self.model(email=email, username=username, **extra_fields)

        # Hash the password before storing (never store plain text passwords)
        user.set_password(password)

        # Save the user to the database
        user.save(using=self._db)

        # Return the created user
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """
        Create and return a superuser with admin privileges.
        
        Superusers have access to Django's admin interface and
        all platform features. Sets is_staff and is_superuser to True.
        
        Args:
            email: Superuser's email address
            username: Superuser's username
            password: Superuser's password
            **extra_fields: Additional fields
        
        Returns:
            CustomUser: The newly created superuser instance
        """
        # Set default values for superuser flags
        extra_fields.setdefault('is_staff', True)       # Can access admin site
        extra_fields.setdefault('is_superuser', True)   # Has all permissions
        extra_fields.setdefault('role', 'admin')         # Set role to admin

        # Validate superuser flags
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Create using the regular create_user method
        return self.create_user(email, username, password, **extra_fields)
