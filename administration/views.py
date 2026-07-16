from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request, pk=None):
    return render(request, 'administration/dashboard.html')

@login_required
def user_management(request, pk=None):
    return render(request, 'administration/user_management.html')

@login_required
def user_detail(request, pk=None):
    return render(request, 'administration/user_detail.html')

@login_required
def internship_moderation(request, pk=None):
    return render(request, 'administration/internship_moderation.html')

@login_required
def company_management(request, pk=None):
    return render(request, 'administration/company_management.html')

@login_required
def activity_logs(request, pk=None):
    return render(request, 'administration/activity_logs.html')

@login_required
def platform_settings(request, pk=None):
    return render(request, 'administration/platform_settings.html')
