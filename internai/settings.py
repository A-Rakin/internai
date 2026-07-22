"""
============================================================
InternAI - Django Project Settings
============================================================
This file contains all configuration settings for the InternAI
Django project including database, installed apps, middleware,
template configuration, static files, and authentication settings.
============================================================
"""

# Import the Path class for cross-platform file path handling
from pathlib import Path

# Import os module for environment variable access
import os

# ============================================================
# BASE DIRECTORY
# ============================================================
from decouple import config, Csv

# Build the base directory path - this points to the project root
# where manage.py is located. All other paths are relative to this.
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================
# SECURITY SETTINGS
# ============================================================
SECRET_KEY = config('SECRET_KEY', default='django-insecure-internai-dev-key-change-in-production-2026!')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*', cast=Csv())
CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='https://*.ngrok-free.app,https://*.ngrok-free.dev,https://*.ngrok.io,http://127.0.0.1,http://localhost',
    cast=Csv()
)


# ============================================================
# APPLICATION DEFINITION
# ============================================================
# All Django apps installed in this project, organized by category

INSTALLED_APPS = [
    # ----- Django Built-in Apps -----
    # Admin interface for managing database records
    'django.contrib.admin',
    # Authentication framework for user login/logout/permissions
    'django.contrib.auth',
    # Content types framework for generic relations
    'django.contrib.contenttypes',
    # Session framework for storing user session data
    'django.contrib.sessions',
    # Messaging framework for one-time notifications
    'django.contrib.messages',
    # Static file serving framework
    'django.contrib.staticfiles',
    # Humanize template filters (e.g., naturaltime, intcomma)
    'django.contrib.humanize',

    # ----- Third-Party Apps -----
    # Crispy forms for beautiful Bootstrap 5 form rendering
    'crispy_forms',
    # Bootstrap 5 template pack for crispy forms
    'crispy_bootstrap5',
    # Widget tweaks for fine-tuning form field HTML attributes
    'widget_tweaks',

    # ----- InternAI Custom Apps -----
    # User authentication and profile management
    'accounts.apps.AccountsConfig',
    # Student portal and student-specific features
    'students.apps.StudentsConfig',
    # Company portal and recruitment management
    'companies.apps.CompaniesConfig',
    # Supervisor portal and evaluation features
    'supervisors.apps.SupervisorsConfig',
    # Internship listing and management
    'internships.apps.InternshipsConfig',
    # Application submission and tracking
    'applications.apps.ApplicationsConfig',
    # Interview scheduling and management
    'interviews.apps.InterviewsConfig',
    # Weekly report submission and review
    'reports.apps.ReportsConfig',
    # In-app notification delivery
    'notifications.apps.NotificationsConfig',
    # Analytics and data visualization
    'analytics.apps.AnalyticsConfig',
    # Document upload and storage
    'documents.apps.DocumentsConfig',
    # Admin portal for platform management
    'administration.apps.AdministrationConfig',
    # Common utilities shared across apps
    'common.apps.CommonConfig',
    # Billing & Stripe Payments
    'billing.apps.BillingConfig',
]

# ============================================================
# MIDDLEWARE CONFIGURATION
# ============================================================
# Middleware processes requests/responses in order (top to bottom for requests,
# bottom to top for responses)

MIDDLEWARE = [
    # Security middleware - adds security headers to responses
    'django.middleware.security.SecurityMiddleware',
    # Session middleware - enables session support
    'django.contrib.sessions.middleware.SessionMiddleware',
    # Common middleware - handles URL rewriting and content length
    'django.middleware.common.CommonMiddleware',
    # CSRF middleware - protects against Cross-Site Request Forgery attacks
    'django.middleware.csrf.CsrfViewMiddleware',
    # Authentication middleware - associates users with requests
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # Message middleware - enables the messaging framework
    'django.contrib.messages.middleware.MessageMiddleware',
    # Clickjacking protection - prevents the site from being framed
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ============================================================
# URL CONFIGURATION
# ============================================================
# Points to the root URL configuration module
ROOT_URLCONF = 'internai.urls'

# ============================================================
# TEMPLATE CONFIGURATION
# ============================================================
# Settings for Django's template engine

TEMPLATES = [
    {
        # Use Django's built-in template engine
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Directories where Django looks for templates (in order)
        'DIRS': [
            # Global templates directory at project root
            BASE_DIR / 'templates',
        ],
        # Automatically discover templates in each app's 'templates/' directory
        'APP_DIRS': True,
        # Template context processors - add variables to every template context
        'OPTIONS': {
            'context_processors': [
                # Adds 'debug' and 'sql_queries' to context
                'django.template.context_processors.debug',
                # Adds 'request' object to context
                'django.template.context_processors.request',
                # Adds 'user' and 'perms' to context
                'django.contrib.auth.context_processors.auth',
                # Adds 'messages' to context for flash messages
                'django.contrib.messages.context_processors.messages',
                # Adds 'MEDIA_URL' to context for media file URLs
                'django.template.context_processors.media',
                # Custom context processor for unread notifications and user role
                'common.context_processors.global_context',
            ],
        },
    },
]

# ============================================================
# WSGI CONFIGURATION
# ============================================================
# Points to the WSGI application for deployment
WSGI_APPLICATION = 'internai.wsgi.application'

# ============================================================
# DATABASE CONFIGURATION
# ============================================================
# Using MySQL via XAMPP for development
# Ensure XAMPP MySQL service is running before starting Django

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME', default='internai_db'),
        'USER': config('DB_USER', default='root'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='127.0.0.1'),
        'PORT': config('DB_PORT', default='3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# ============================================================
# PASSWORD VALIDATION
# ============================================================
# Validators that check password strength during user registration
# and password changes

AUTH_PASSWORD_VALIDATORS = [
    {
        # Checks that password is not too similar to user attributes
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        # Enforces minimum password length (default: 8 characters)
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        # Rejects passwords that are too common (e.g., 'password123')
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        # Rejects passwords that are entirely numeric
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ============================================================
# INTERNATIONALIZATION
# ============================================================
# Language and timezone settings

# Default language for the application
LANGUAGE_CODE = 'en-us'

# Timezone - set to Bangladesh Standard Time (UTC+6)
TIME_ZONE = 'Asia/Dhaka'

# Enable Django's translation system
USE_I18N = True

# Enable timezone-aware datetime objects
USE_TZ = True

# ============================================================
# STATIC FILES CONFIGURATION
# ============================================================
# Settings for serving CSS, JavaScript, images, and other static assets

# URL prefix for static files in templates (e.g., {% static 'css/main.css' %})
STATIC_URL = '/static/'

# Additional directories where Django looks for static files
# beyond each app's 'static/' directory
STATICFILES_DIRS = [
    # Global static files directory at project root
    BASE_DIR / 'static',
]

# Directory where 'collectstatic' gathers all static files for production
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ============================================================
# MEDIA FILES CONFIGURATION
# ============================================================
# Settings for user-uploaded files (resumes, avatars, documents, etc.)

# URL prefix for accessing uploaded media files
MEDIA_URL = '/media/'

# Directory where uploaded files are stored on the filesystem
MEDIA_ROOT = BASE_DIR / 'media'

# ============================================================
# AUTHENTICATION SETTINGS
# ============================================================
# Custom user model and authentication redirects

# Use our custom User model instead of Django's default User
AUTH_USER_MODEL = 'accounts.CustomUser'

# URL to redirect to after successful login
LOGIN_URL = '/accounts/login/'

# URL to redirect to after successful login (default redirect)
LOGIN_REDIRECT_URL = '/accounts/redirect/'

# URL to redirect to after logout
LOGOUT_REDIRECT_URL = '/'

# ============================================================
# CRISPY FORMS CONFIGURATION
# ============================================================
# Settings for django-crispy-forms Bootstrap 5 integration

# Use Bootstrap 5 as the default template pack for crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# ============================================================
# DEFAULT AUTO FIELD
# ============================================================
# Default primary key field type for models without explicit primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================================
# EMAIL CONFIGURATION (Development)
# ============================================================
# Console backend prints emails to terminal instead of sending them
# Replace with SMTP backend for production email delivery
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ============================================================
# MESSAGE TAGS
# ============================================================
# Map Django message levels to Bootstrap CSS alert classes
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',      # Debug messages - gray
    messages.INFO: 'alert-info',            # Info messages - blue
    messages.SUCCESS: 'alert-success',      # Success messages - green
    messages.WARNING: 'alert-warning',      # Warning messages - yellow
    messages.ERROR: 'alert-danger',         # Error messages - red
}

# ============================================================
# STRIPE PAYMENT GATEWAY CONFIGURATION
# ============================================================
STRIPE_PUBLIC_KEY = config('STRIPE_PUBLIC_KEY', default='')
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', default='')
STRIPE_WEBHOOK_SECRET = config('STRIPE_WEBHOOK_SECRET', default='')

# ============================================================
# GROQ CLOUD AI API CONFIGURATION
# ============================================================
GROQ_API_KEY = config('GROQ_API_KEY', default='')


