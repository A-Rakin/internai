#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.
This file is the entry point for running Django management commands
such as runserver, migrate, makemigrations, createsuperuser, etc.
"""

# Import the os module to interact with the operating system
import os

# Import the sys module to access command-line arguments
import sys


def main():
    """
    Main function that sets up Django settings and executes
    management commands from the command line.
    """
    # Set the default Django settings module to our project's settings
    # This tells Django where to find the configuration
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'internai.settings')

    try:
        # Import Django's command-line execution utility
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # If Django is not installed, raise a helpful error message
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Execute the management command passed via command-line arguments
    # sys.argv contains the command-line arguments (e.g., ['manage.py', 'runserver'])
    execute_from_command_line(sys.argv)


# Standard Python idiom to ensure main() runs only when the script is executed directly
if __name__ == '__main__':
    main()
