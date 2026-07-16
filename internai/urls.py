"""
============================================================
InternAI - Root URL Configuration
============================================================
This file maps URL patterns to their corresponding Django app
URL configurations. Each app has its own urls.py that handles
the detailed routing for that module.
============================================================
"""

# Import the admin site for Django's built-in admin interface
from django.contrib import admin

# Import path for defining URL patterns and include for referencing app URLs
from django.urls import path, include

# Import settings and static for serving media files during development
from django.conf import settings
from django.conf.urls.static import static

# ============================================================
# URL PATTERNS
# ============================================================
# Each path maps a URL prefix to an app's URL configuration.
# The 'include()' function delegates URL handling to the specified app.

urlpatterns = [
    # ----- Django Admin -----
    # Built-in admin interface at /admin/
    path('admin/', admin.site.urls),

    # ----- Public Landing Pages -----
    # Landing website pages (home, about, features, etc.) at root URL
    path('', include('common.urls', namespace='landing')),

    # ----- Authentication -----
    # Login, register, logout, password management at /accounts/
    path('accounts/', include('accounts.urls', namespace='accounts')),

    # ----- Student Portal -----
    # Student dashboard and features at /student/
    path('student/', include('students.urls', namespace='students')),

    # ----- Company Portal -----
    # Company dashboard and recruitment at /company/
    path('company/', include('companies.urls', namespace='companies')),

    # ----- Supervisor Portal -----
    # Supervisor dashboard and evaluations at /supervisor/
    path('supervisor/', include('supervisors.urls', namespace='supervisors')),

    # ----- Internship Browsing -----
    # Public internship listings at /internships/
    path('internships/', include('internships.urls', namespace='internships')),

    # ----- Applications -----
    # Application management at /applications/
    path('applications/', include('applications.urls', namespace='applications')),

    # ----- Interviews -----
    # Interview scheduling at /interviews/
    path('interviews/', include('interviews.urls', namespace='interviews')),

    # ----- Reports -----
    # Weekly report management at /reports/
    path('reports/', include('reports.urls', namespace='reports')),

    # ----- Notifications -----
    # Notification system at /notifications/
    path('notifications/', include('notifications.urls', namespace='notifications')),

    # ----- Analytics -----
    # Analytics dashboards at /analytics/
    path('analytics/', include('analytics.urls', namespace='analytics')),

    # ----- Documents -----
    # Document management at /documents/
    path('documents/', include('documents.urls', namespace='documents')),

    # ----- Administration -----
    # Admin portal at /administration/
    path('administration/', include('administration.urls', namespace='administration')),
]

# ============================================================
# MEDIA FILE SERVING (Development Only)
# ============================================================
# In development, Django serves uploaded media files directly.
# In production, configure your web server (Nginx/Apache) to serve these.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
