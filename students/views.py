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

    # Check 7-day package expiry reminder
    try:
        from billing.views import check_and_notify_expiring_packages
        check_and_notify_expiring_packages(request.user)
    except Exception:
        pass

    subscription = profile.get_active_subscription()

    context = {
        'profile': profile,
        'subscription': subscription,
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
    """Display student profile with evaluations and subscription status."""
    student_profile = get_object_or_404(StudentProfile, user=request.user)
    subscription = student_profile.get_active_subscription()

    from reports.models import Evaluation
    evaluations_list = Evaluation.objects.filter(student=student_profile).select_related('supervisor__user', 'internship').order_by('-created_at')

    context = {
        'profile': student_profile,
        'subscription': subscription,
        'evaluations': evaluations_list,
    }
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
                try:
                    from common.validators import validate_image_file
                    validate_image_file(request.FILES['avatar'])
                    request.user.avatar = request.FILES['avatar']
                except Exception as ve:
                    messages.error(request, str(ve).strip("['']"))
                    return render(request, 'students/profile_edit.html', {'form': form, 'profile': student_profile})
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
    """List all weekly reports and supervisor performance evaluations."""
    student_profile = get_object_or_404(StudentProfile, user=request.user)
    reports_list = WeeklyReport.objects.filter(student=student_profile).select_related('internship').order_by('-week_number')

    from reports.models import Evaluation
    evaluations_list = Evaluation.objects.filter(student=student_profile).select_related('supervisor__user', 'internship').order_by('-created_at')

    context = {
        'reports': reports_list,
        'evaluations': evaluations_list,
    }
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
            try:
                from common.validators import validate_image_file
                validate_image_file(request.FILES['avatar'])
                request.user.avatar = request.FILES['avatar']
                request.user.save()
                messages.success(request, 'Profile photo updated.')
            except Exception as ve:
                messages.error(request, str(ve).strip("['']"))

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


@login_required
@role_required('student')
def withdraw_application(request, pk=None):
    """Allow a student to withdraw/resign an accepted placement or application."""
    student_profile = get_object_or_404(StudentProfile, user=request.user)
    app_obj = get_object_or_404(Application, pk=pk, student=student_profile)

    if request.method == 'POST':
        prev_status = app_obj.status
        app_obj.status = 'withdrawn'
        app_obj.save(update_fields=['status'])

        company_user = app_obj.internship.company.user
        comp_name = app_obj.internship.company.company_name

        # Notify Company
        Notification.objects.create(
            recipient=company_user,
            notification_type='application',
            title=f'Placement Withdrawn: {request.user.get_full_name()}',
            message=f'{request.user.get_full_name()} has withdrawn/resigned their application for "{app_obj.internship.title}".',
            link=f'/company/applicant-detail/{app_obj.pk}/',
        )

        # Notify Supervisor if assigned
        if app_obj.assigned_supervisor:
            Notification.objects.create(
                recipient=app_obj.assigned_supervisor.user,
                notification_type='system',
                title=f'Placement Resignation: {request.user.get_full_name()}',
                message=f'Student {request.user.get_full_name()} has withdrawn from their placement at {comp_name}.',
                link=f'/supervisors/students/{student_profile.pk}/',
            )

        # If student's current active supervisor was linked to this placement, clear if no other accepted placements
        other_active = Application.objects.filter(student=student_profile, status='accepted').exists()
        if not other_active:
            student_profile.supervisor = None
            student_profile.save(update_fields=['supervisor'])

        messages.success(
            request,
            f'Successfully withdrawn your application for "{app_obj.internship.title}" at {comp_name}. '
            f'Your placement status is now open to accept or get assigned to another offer.'
        )
        return redirect('students:applications')

    context = {'application': app_obj}
    return render(request, 'students/withdraw_confirm.html', context)


@login_required
@role_required('student')
def update_supervisor(request):
    """Allow student to change/update their listed Academic Supervisor."""
    student_profile = get_object_or_404(StudentProfile, user=request.user)

    if request.method == 'POST':
        supervisor_email = request.POST.get('supervisor_email', '').strip().lower()
        if not supervisor_email:
            messages.error(request, 'Please enter a valid supervisor email address.')
            return redirect('students:applications')

        from accounts.models import CustomUser, SupervisorProfile
        sup_user = CustomUser.objects.filter(email__iexact=supervisor_email, role=CustomUser.SUPERVISOR).first()

        if sup_user and hasattr(sup_user, 'supervisor_profile'):
            sup_profile = sup_user.supervisor_profile
            if sup_profile.is_at_capacity():
                messages.error(
                    request,
                    f'Cannot assign supervisor {supervisor_email}: Supervisor has reached the maximum capacity limit of 5 assigned students. '
                    f'Please enter a different academic supervisor email.'
                )
            else:
                student_profile.supervisor = sup_profile
                student_profile.save(update_fields=['supervisor'])

                # Update assigned supervisor on active accepted applications
                Application.objects.filter(student=student_profile, status='accepted').update(assigned_supervisor=sup_profile, supervisor_email=supervisor_email)

                # Notify Supervisor
                Notification.objects.create(
                    recipient=sup_user,
                    notification_type='system',
                    title=f'🎓 Student Supervision Link: {request.user.get_full_name()}',
                    message=f'{request.user.get_full_name()} ({student_profile.university}) has updated their Academic Supervisor to you.',
                    link=f'/supervisors/students/{student_profile.pk}/',
                )

                messages.success(request, f'Academic Supervisor updated successfully to {sup_user.get_full_name()} ({supervisor_email}).')
        else:
            messages.warning(
                request,
                f"Supervisor email '{supervisor_email}' recorded. However, no active supervisor account was found. "
                f"Please tell your supervisor to register on InternAI with '{supervisor_email}'."
            )

        return redirect('students:applications')

    return redirect('students:applications')

