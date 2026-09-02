"""
============================================================
Companies Views - Company Portal Operations
============================================================
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Q

from accounts.decorators import role_required
from accounts.models import CompanyProfile
from internships.models import Internship, InternshipCategory
from applications.models import Application
from interviews.models import Interview
from notifications.models import Notification
from companies.forms import (
    CompanyProfileForm, InternshipForm,
    InterviewScheduleForm, ApplicationStatusForm,
)


@login_required
@role_required('company')
def dashboard(request):
    """Company dashboard with recruitment stats."""
    company = get_object_or_404(CompanyProfile, user=request.user)

    internships = Internship.objects.filter(company=company)
    total_applications = Application.objects.filter(internship__company=company)

    stats = {
        'total_internships': internships.count(),
        'active_internships': internships.filter(status='open', is_approved=True).count(),
        'total_applicants': total_applications.count(),
        'pending_review': total_applications.filter(status='pending').count(),
        'interviews_scheduled': Interview.objects.filter(
            application__internship__company=company,
            outcome='pending',
        ).count(),
    }

    recent_applications = total_applications.select_related(
        'student__user', 'internship'
    ).order_by('-applied_at')[:10]

    recent_notifications = Notification.objects.filter(recipient=request.user, is_read=False)[:5]

    context = {
        'company': company,
        'stats': stats,
        'recent_applications': recent_applications,
        'recent_notifications': recent_notifications,
    }
    return render(request, 'companies/dashboard.html', context)


@login_required
@role_required('company')
def profile(request):
    """Display company profile."""
    company = get_object_or_404(CompanyProfile, user=request.user)
    context = {'company': company}
    return render(request, 'companies/profile.html', context)


@login_required
@role_required('company')
def profile_edit(request, pk=None):
    """Edit company profile."""
    company = get_object_or_404(CompanyProfile, user=request.user)

    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, request.FILES, instance=company, user=request.user)
        if 'logo' in request.FILES:
            try:
                from common.validators import validate_image_file
                validate_image_file(request.FILES['logo'])
            except Exception as ve:
                messages.error(request, str(ve).strip("['']"))
                return render(request, 'companies/profile_edit.html', {'form': form, 'company': company})

        if form.is_valid():
            form.save()
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.phone = form.cleaned_data['phone']
            request.user.save()
            messages.success(request, 'Company profile updated successfully!')
            return redirect('companies:profile')
    else:
        form = CompanyProfileForm(instance=company, user=request.user)

    context = {'form': form, 'company': company}
    return render(request, 'companies/profile_edit.html', context)


@login_required
@role_required('company')
def internship_create(request):
    """Create a new internship listing."""
    company = get_object_or_404(CompanyProfile, user=request.user)

    if request.method == 'POST':
        form = InternshipForm(request.POST)
        if form.is_valid():
            internship = form.save(commit=False)
            internship.company = company
            internship.status = 'draft'
            internship.save()
            messages.success(request, f'Internship "{internship.title}" created! It will be visible once approved by admin.')
            return redirect('companies:internship_list')
    else:
        form = InternshipForm()

    context = {'form': form, 'action': 'Create'}
    return render(request, 'companies/internship_create.html', context)


@login_required
@role_required('company')
def internship_edit(request, pk=None):
    """Edit an existing internship listing."""
    company = get_object_or_404(CompanyProfile, user=request.user)
    internship = get_object_or_404(Internship, pk=pk, company=company)

    if internship.is_approved:
        messages.error(request, 'This internship post has been verified and approved by admin and can no longer be edited.')
        return redirect('companies:internship_list')

    if request.method == 'POST':
        form = InternshipForm(request.POST, instance=internship)
        if form.is_valid():
            form.save()
            messages.success(request, 'Internship updated successfully!')
            return redirect('companies:internship_list')
    else:
        form = InternshipForm(instance=internship)

    context = {'form': form, 'internship': internship, 'action': 'Edit'}
    return render(request, 'companies/internship_edit.html', context)


@login_required
@role_required('company')
def internship_delete(request, pk=None):
    """Delete an unapproved internship listing."""
    company = get_object_or_404(CompanyProfile, user=request.user)
    internship = get_object_or_404(Internship, pk=pk, company=company)

    if internship.is_approved:
        messages.error(request, 'Approved internships cannot be deleted by the company.')
        return redirect('companies:internship_list')

    if request.method == 'POST':
        title = internship.title
        internship.delete()
        messages.success(request, f'Internship "{title}" has been deleted successfully.')
        return redirect('companies:internship_list')

    return redirect('companies:internship_list')


@login_required
@role_required('company')
def internship_list(request):
    """List all internships posted by this company."""
    company = get_object_or_404(CompanyProfile, user=request.user)
    status_filter = request.GET.get('status', '')

    internships = Internship.objects.filter(company=company).annotate(
        application_count=Count('applications')
    )
    if status_filter:
        internships = internships.filter(status=status_filter)

    context = {
        'internships': internships.order_by('-created_at'),
        'status_filter': status_filter,
    }
    return render(request, 'companies/internship_list.html', context)


@login_required
@role_required('company')
def applicants(request):
    """List all applicants for this company's internships."""
    company = get_object_or_404(CompanyProfile, user=request.user)
    status_filter = request.GET.get('status', '')
    internship_filter = request.GET.get('internship', '')

    apps = Application.objects.filter(
        internship__company=company
    ).select_related('student__user', 'internship')

    if status_filter:
        apps = apps.filter(status=status_filter)
    if internship_filter:
        apps = apps.filter(internship_id=internship_filter)

    internships = Internship.objects.filter(company=company)

    context = {
        'applications': apps.order_by('-applied_at'),
        'internships': internships,
        'status_filter': status_filter,
        'internship_filter': internship_filter,
    }
    return render(request, 'companies/applicants.html', context)


@login_required
@role_required('company')
def applicant_detail(request, pk=None):
    """View applicant details and update application status."""
    company = get_object_or_404(CompanyProfile, user=request.user)
    application = get_object_or_404(Application, pk=pk, internship__company=company)

    if request.method == 'POST':
        form = ApplicationStatusForm(request.POST)
        if form.is_valid():
            application.status = form.cleaned_data['status']
            application.company_notes = form.cleaned_data['company_notes']
            if form.cleaned_data['rejection_reason']:
                application.rejection_reason = form.cleaned_data['rejection_reason']
            application.save()

            # Create notification for the student
            Notification.objects.create(
                recipient=application.student.user,
                notification_type='application',
                title=f'Application Update: {application.internship.title}',
                message=f'Your application status has been updated to: {application.get_status_display()}',
                link=f'/student/application-detail/{application.pk}/',
            )
            messages.success(request, 'Application status updated.')
            return redirect('companies:applicant_detail', pk=pk)
    else:
        form = ApplicationStatusForm(initial={
            'status': application.status,
            'company_notes': application.company_notes,
            'rejection_reason': application.rejection_reason,
        })

    interviews_list = Interview.objects.filter(application=application).order_by('-scheduled_at')

    context = {
        'application': application,
        'form': form,
        'interviews': interviews_list,
    }
    return render(request, 'companies/applicant_detail.html', context)


@login_required
@role_required('company')
def interviews(request):
    """List all interviews for this company."""
    company = get_object_or_404(CompanyProfile, user=request.user)
    interviews_list = Interview.objects.filter(
        application__internship__company=company
    ).select_related('application__student__user', 'application__internship').order_by('-scheduled_at')

    context = {'interviews': interviews_list}
    return render(request, 'companies/interviews.html', context)


@login_required
@role_required('company')
def interview_schedule(request, pk=None):
    """Schedule a new interview for an application."""
    company = get_object_or_404(CompanyProfile, user=request.user)
    application = get_object_or_404(Application, pk=pk, internship__company=company)

    if request.method == 'POST':
        form = InterviewScheduleForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.application = application
            interview.save()

            # Update application status to 'interview'
            application.status = 'interview'
            application.save()

            # Notify student
            Notification.objects.create(
                recipient=application.student.user,
                notification_type='interview',
                title=f'Interview Scheduled: {application.internship.title}',
                message=f'An interview has been scheduled for {interview.scheduled_at.strftime("%B %d, %Y at %I:%M %p")}',
                link=f'/student/applications/',
                priority='high',
            )
            messages.success(request, 'Interview scheduled successfully!')
            return redirect('companies:applicant_detail', pk=pk)
    else:
        form = InterviewScheduleForm()

    context = {
        'form': form,
        'application': application,
    }
    return render(request, 'companies/interview_schedule.html', context)


@login_required
@role_required('company')
def ai_resume_analysis(request):
    """AI Resume Analysis & Candidate Ranking page (Position Specific)."""
    company = get_object_or_404(CompanyProfile, user=request.user)
    company_internships = Internship.objects.filter(company=company).order_by('-created_at')

    internship_id = request.GET.get('internship_id', '')
    selected_internship = None

    ranked_applications = Application.objects.filter(
        internship__company=company
    ).select_related('student__user', 'internship', 'student')

    if internship_id:
        selected_internship = get_object_or_404(Internship, pk=internship_id, company=company)
        ranked_applications = ranked_applications.filter(internship=selected_internship)

    ranked_applications = ranked_applications.order_by('-ai_match_score', '-applied_at')

    context = {
        'company': company,
        'company_internships': company_internships,
        'selected_internship': selected_internship,
        'selected_internship_id': int(internship_id) if internship_id and internship_id.isdigit() else '',
        'ranked_applications': ranked_applications,
    }
    return render(request, 'companies/ai_resume_analysis.html', context)


@login_required
@role_required('company')
def ai_candidate_ranking(request):
    """AI Candidate Ranking page."""
    return ai_resume_analysis(request)


@login_required
@role_required('company')
def settings(request):
    """Company account settings."""
    company = get_object_or_404(CompanyProfile, user=request.user)

    if request.method == 'POST':
        phone = request.POST.get('phone', '').strip()
        request.user.phone = phone
        if 'avatar' in request.FILES:
            try:
                from common.validators import validate_image_file
                validate_image_file(request.FILES['avatar'])
                request.user.avatar = request.FILES['avatar']
            except Exception as ve:
                messages.error(request, str(ve).strip("['']"))
                return render(request, 'companies/settings.html', {'company': company})
        request.user.save()
        messages.success(request, 'Settings saved successfully.')
        return redirect('companies:settings')

    context = {'company': company}
    return render(request, 'companies/settings.html', context)
