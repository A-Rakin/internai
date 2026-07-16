from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def browse(request, pk=None, internship_id=None):
    return render(request, 'internships/browse.html')

@login_required
def detail(request, pk=None, internship_id=None):
    return render(request, 'internships/detail.html')

@login_required
def search_results(request, pk=None, internship_id=None):
    return render(request, 'internships/search_results.html')
