from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request, pk=None):
    return render(request, 'companies/dashboard.html')

@login_required
def profile(request, pk=None):
    return render(request, 'companies/profile.html')

@login_required
def profile_edit(request, pk=None):
    return render(request, 'companies/profile_edit.html')

@login_required
def internship_create(request, pk=None):
    return render(request, 'companies/internship_create.html')

@login_required
def internship_edit(request, pk=None):
    return render(request, 'companies/internship_edit.html')

@login_required
def internship_list(request, pk=None):
    return render(request, 'companies/internship_list.html')

@login_required
def applicants(request, pk=None):
    return render(request, 'companies/applicants.html')

@login_required
def applicant_detail(request, pk=None):
    return render(request, 'companies/applicant_detail.html')

@login_required
def interviews(request, pk=None):
    return render(request, 'companies/interviews.html')

@login_required
def interview_schedule(request, pk=None):
    return render(request, 'companies/interview_schedule.html')

@login_required
def ai_resume_analysis(request, pk=None):
    return render(request, 'companies/ai_resume_analysis.html')

@login_required
def ai_candidate_ranking(request, pk=None):
    return render(request, 'companies/ai_candidate_ranking.html')

@login_required
def settings(request, pk=None):
    return render(request, 'companies/settings.html')
