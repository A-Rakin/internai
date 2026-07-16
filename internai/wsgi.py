"""
============================================================
InternAI - WSGI Configuration
============================================================
WSGI (Web Server Gateway Interface) is the standard interface
between web servers and Python web applications. This file
exposes the WSGI callable as a module-level variable named 'application'.
Used by production servers like Gunicorn or uWSGI.
============================================================
"""

# Import os for environment variable management
import os

# Import Django's WSGI handler
from django.core.wsgi import get_wsgi_application

# Set the Django settings module for the WSGI application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'internai.settings')

# Create the WSGI application object that the web server will use
application = get_wsgi_application()
