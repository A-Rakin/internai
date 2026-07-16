from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request, pk=None):
    return render(request, 'students/dashboard.html')

@login_required
def profile(request, pk=None):
    return render(request, 'students/profile.html')

@login_required
def profile_edit(request, pk=None):
    return render(request, 'students/profile_edit.html')

@login_required
def applications(request, pk=None):
    return render(request, 'students/applications.html')

@login_required
def application_detail(request, pk=None):
    return render(request, 'students/application_detail.html')

@login_required
def interviews(request, pk=None):
    return render(request, 'students/interviews.html')

@login_required
def reports(request, pk=None):
    return render(request, 'students/reports.html')

@login_required
def report_submit(request, pk=None):
    return render(request, 'students/report_submit.html')

@login_required
def settings(request, pk=None):
    return render(request, 'students/settings.html')
