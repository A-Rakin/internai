from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def submit(request, pk=None, internship_id=None):
    return render(request, 'applications/submit.html')

@login_required
def list(request, pk=None, internship_id=None):
    return render(request, 'applications/list.html')

@login_required
def detail(request, pk=None, internship_id=None):
    return render(request, 'applications/detail.html')
