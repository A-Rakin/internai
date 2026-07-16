"""
============================================================
InternAI - ASGI Configuration
============================================================
ASGI (Asynchronous Server Gateway Interface) is the successor
to WSGI, supporting async protocols like WebSockets.
Used by async servers like Daphne or Uvicorn.
============================================================
"""

# Import os for environment variable management
import os

# Import Django's ASGI handler
from django.core.asgi import get_asgi_application

# Set the Django settings module for the ASGI application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'internai.settings')

# Create the ASGI application object
application = get_asgi_application()
