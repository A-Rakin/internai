"""
============================================================
Analytics Views - Analytics & Insights Dashboard
============================================================
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from internships.models import Internship
from applications.models import Application
from accounts.models import CustomUser, StudentProfile, CompanyProfile


@login_required
def dashboard(request):
    """Analytics dashboard with visualizations data."""
    context = {
        'total_users': CustomUser.objects.count(),
        'total_internships': Internship.objects.count(),
        'total_applications': Application.objects.count(),
        'open_positions': Internship.objects.filter(status='open', is_approved=True).count(),
    }
    return render(request, 'analytics/dashboard.html', context)
