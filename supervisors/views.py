from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request, pk=None):
    return render(request, 'supervisors/dashboard.html')

@login_required
def students_list(request, pk=None):
    return render(request, 'supervisors/students_list.html')

@login_required
def student_detail(request, pk=None):
    return render(request, 'supervisors/student_detail.html')

@login_required
def report_review(request, pk=None):
    return render(request, 'supervisors/report_review.html')

@login_required
def evaluation(request, pk=None):
    return render(request, 'supervisors/evaluation.html')

@login_required
def settings(request, pk=None):
    return render(request, 'supervisors/settings.html')
