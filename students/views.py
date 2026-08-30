"""
============================================================
Students Views - Student Portal Operations
============================================================
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Q

from accounts.decorators import role_required
from accounts.models import StudentProfile
from applications.models import Application
from internships.models import Internship
from interviews.models import Interview
from reports.models import WeeklyReport
from notifications.models import Notification
from students.forms import StudentProfileForm, WeeklyReportForm


@login_required
@role_required('student')
def dashboard(request):
    """Student dashboard with stats and recent activity."""
    profile = get_object_or_404(StudentProfile, user=request.user)

    # Application stats
    applications = Application.objects.filter(student=profile)
    app_stats = {
        'total': applications.count(),
        'pending': applications.filter(status='pending').count(),
        'reviewing': applications.filter(status__in=['reviewing', 'assessment']).count(),
        'interview': applications.filter(status='interview').count(),
        'accepted': applications.filter(status='accepted').count(),
        'rejected': applications.filter(status='rejected').count(),
    }

    # Upcoming interviews
    upcoming_interviews = Interview.objects.filter(
        application__student=profile,
        scheduled_at__gte=timezone.now(),
        outcome='pending',
    ).select_related('application__internship').order_by('scheduled_at')[:5]

    # Recent applications
    recent_applications = applications.select_related('internship__company').order_by('-applied_at')[:5]

    # Recent notifications
    recent_notifications = Notification.objects.filter(recipient=request.user, is_read=False)[:5]

    # Reports stats
    reports = WeeklyReport.objects.filter(student=profile)
    report_stats = {
        'total': reports.count(),
        'pending': reports.filter(status='submitted').count(),
        'approved': reports.filter(status='approved').count(),
    }

    context = {
        'profile': profile,
        'app_stats': app_stats,
        'upcoming_interviews': upcoming_interviews,
        'recent_applications': recent_applications,
        'recent_notifications': recent_notifications,
        'report_stats': report_stats,
    }
    return render(request, 'students/dashboard.html', context)


@login_required
@role_required('student')
def profile(request):
    """Display student profile."""
    student_profile = get_object_or_404(StudentProfile, user=request.user)
    context = {'profile': student_profile}
    return render(request, 'students/profile.html', context)


@login_required
@role_required('student')
def profile_edit(request, pk=None):
    """Edit student profile."""
    student_profile = get_object_or_404(StudentProfile, user=request.user)

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student_profile, user=request.user)
        if form.is_valid():
            form.save()
            # Update user fields
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.phone = form.cleaned_data['phone']
            if 'avatar' in request.FILES:
                request.user.avatar = request.FILES['avatar']
            request.user.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('students:profile')
    else:
        form = StudentProfileForm(instance=student_profile, user=request.user)

    context = {'form': form, 'profile': student_profile}
    return render(request, 'students/profile_edit.html', context)


@login_required
@role_required('student')
def applications(request):
    """List all student applications."""
    student_profile = get_object_or_404(StudentProfile, user=request.user)
    status_filter = request.GET.get('status', '')

    apps = Application.objects.filter(student=student_profile).select_related('internship__company')
    if status_filter:
        apps = apps.filter(status=status_filter)

    context = {
        'applications': apps.order_by('-applied_at'),
        'status_filter': status_filter,
    }
    return render(request, 'students/applications.html', context)


@login_required
@role_required('student')
def application_detail(request, pk=None):
    """View single application detail."""
    student_profile = get_object_or_404(StudentProfile, user=request.user)
    application = get_object_or_404(Application, pk=pk, student=student_profile)
    interviews_list = Interview.objects.filter(application=application).order_by('-scheduled_at')

    context = {
        'application': application,
        'interviews': interviews_list,
    }
    return render(request, 'students/application_detail.html', context)


@login_required
@role_required('student')
def interviews(request):
    """List all interviews for this student."""
    student_profile = get_object_or_404(StudentProfile, user=request.user)
    interviews_list = Interview.objects.filter(
        application__student=student_profile
    ).select_related('application__internship__company').order_by('-scheduled_at')

    context = {'interviews': interviews_list}
    return render(request, 'students/interviews.html', context)


@login_required
@role_required('student')
def reports(request):
    """List all weekly reports."""
    student_profile = get_object_or_404(StudentProfile, user=request.user)
    reports_list = WeeklyReport.objects.filter(student=student_profile).select_related('internship').order_by('-week_number')

    context = {'reports': reports_list}
    return render(request, 'students/reports.html', context)


@login_required
@role_required('student')
def report_submit(request):
    """Submit a new weekly report."""
    student_profile = get_object_or_404(StudentProfile, user=request.user)

    if request.method == 'POST':
        form = WeeklyReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.student = student_profile
            report.status = 'submitted'
            report.submitted_at = timezone.now()
            report.save()
            messages.success(request, f'Week {report.week_number} report submitted successfully!')
            return redirect('students:reports')
    else:
        form = WeeklyReportForm()
        # Only show internships the student has been accepted to
        accepted_internships = Internship.objects.filter(
            applications__student=student_profile,
            applications__status='accepted',
        )
        form.fields['internship'].queryset = accepted_internships

    context = {'form': form}
    return render(request, 'students/report_submit.html', context)


@login_required
@role_required('student')
def settings(request):
    """Student account settings."""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()

        if email and email != request.user.email:
            from accounts.models import CustomUser
            if CustomUser.objects.filter(email=email).exclude(pk=request.user.pk).exists():
                messages.error(request, 'This email is already in use.')
            else:
                request.user.email = email
                request.user.save()
                messages.success(request, 'Email updated successfully.')

        if 'avatar' in request.FILES:
            request.user.avatar = request.FILES['avatar']
            request.user.save()
            messages.success(request, 'Profile photo updated.')

        request.user.phone = phone
        request.user.save()
        messages.success(request, 'Settings saved.')
        return redirect('students:settings')

    return render(request, 'students/settings.html')


@login_required
@role_required('student')
def interview_prep(request, pk=None):
    """AI Interview Prep Coach for a specific interview or internship."""
    from common.ai_engine import generate_interview_questions

    interview = None
    internship = None

    if pk:
        # Check if pk is interview pk or internship pk
        interview = Interview.objects.filter(pk=pk, application__student__user=request.user).first()
        if interview:
            internship = interview.application.internship
        else:
            internship = get_object_or_404(Internship, pk=pk)

    if not internship:
        messages.error(request, 'Internship position not found for practice.')
        return redirect('students:interviews')

    questions = generate_interview_questions(internship)

    context = {
        'interview': interview,
        'internship': internship,
        'questions': questions,
    }
    return render(request, 'students/interview_prep.html', context)


@login_required
@role_required('student')
def interview_prep_grade(request):
    """AJAX endpoint to grade an interview answer."""
    import json
    from django.http import JsonResponse
    from common.ai_engine import grade_interview_answer

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = data.get('question', '')
            answer = data.get('answer', '')
            internship_id = data.get('internship_id')

            internship = get_object_or_404(Internship, pk=internship_id)
            result = grade_interview_answer(question, answer, internship)
            return JsonResponse({'success': True, 'result': result})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
@role_required('student')
def saved_internships(request):
    """View student's saved/bookmarked internships."""
    from internships.models import SavedInternship
    student_profile = get_object_or_404(StudentProfile, user=request.user)
    saved_list = SavedInternship.objects.filter(student=student_profile).select_related('internship__company')

    context = {'saved_list': saved_list}
    return render(request, 'students/saved_internships.html', context)


@login_required
@role_required('student')
def toggle_bookmark(request):
    """AJAX view to toggle bookmarking an internship."""
    import json
    from django.http import JsonResponse
    from internships.models import SavedInternship

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            internship_id = data.get('internship_id')
            student_profile = get_object_or_404(StudentProfile, user=request.user)
            internship = get_object_or_404(Internship, pk=internship_id)

            saved, created = SavedInternship.objects.get_or_create(
                student=student_profile,
                internship=internship,
            )

            if not created:
                saved.delete()
                is_saved = False
            else:
                is_saved = True

            return JsonResponse({'success': True, 'is_saved': is_saved})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)

