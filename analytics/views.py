from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request, pk=None, internship_id=None):
    return render(request, 'analytics/dashboard.html')
