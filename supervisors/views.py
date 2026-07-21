"""
============================================================
Supervisors Views - Supervisor Portal Operations
============================================================
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from accounts.decorators import role_required
from accounts.models import SupervisorProfile, StudentProfile
from reports.models import WeeklyReport, Evaluation
from internships.models import Internship
from notifications.models import Notification
from supervisors.forms import SupervisorProfileForm, ReportReviewForm, EvaluationForm


@login_required
@role_required('supervisor')
def dashboard(request):
    """Supervisor dashboard with overview stats."""
    supervisor = get_object_or_404(SupervisorProfile, user=request.user)

    # Reports assigned to this supervisor
    pending_reports = WeeklyReport.objects.filter(
        supervisor=supervisor, status='submitted'
    ).select_related('student__user', 'internship')

    reviewed_reports = WeeklyReport.objects.filter(
        supervisor=supervisor, status__in=['approved', 'reviewed']
    )

    # Students with reports assigned to this supervisor
    assigned_student_ids = WeeklyReport.objects.filter(
        supervisor=supervisor
    ).values_list('student_id', flat=True).distinct()
    assigned_students = StudentProfile.objects.filter(user_id__in=assigned_student_ids).select_related('user')

    # Evaluations
    evaluations = Evaluation.objects.filter(supervisor=supervisor)

    stats = {
        'assigned_students': assigned_students.count(),
        'pending_reports': pending_reports.count(),
        'reviewed_reports': reviewed_reports.count(),
        'evaluations': evaluations.count(),
    }

    recent_notifications = Notification.objects.filter(recipient=request.user, is_read=False)[:5]

    context = {
        'supervisor': supervisor,
        'stats': stats,
        'pending_reports': pending_reports[:10],
        'assigned_students': assigned_students[:10],
        'recent_notifications': recent_notifications,
    }
    return render(request, 'supervisors/dashboard.html', context)


@login_required
@role_required('supervisor')
def students_list(request):
    """List all students assigned to this supervisor."""
    supervisor = get_object_or_404(SupervisorProfile, user=request.user)

    assigned_student_ids = WeeklyReport.objects.filter(
        supervisor=supervisor
    ).values_list('student_id', flat=True).distinct()

    students = StudentProfile.objects.filter(
        user_id__in=assigned_student_ids
    ).select_related('user')

    context = {'students': students, 'supervisor': supervisor}
    return render(request, 'supervisors/students_list.html', context)


@login_required
@role_required('supervisor')
def student_detail(request, pk=None):
    """View detailed info about a specific student."""
    supervisor = get_object_or_404(SupervisorProfile, user=request.user)
    student = get_object_or_404(StudentProfile, pk=pk)

    reports_list = WeeklyReport.objects.filter(
        student=student, supervisor=supervisor
    ).order_by('-week_number')

    evaluations = Evaluation.objects.filter(
        student=student, supervisor=supervisor
    ).order_by('-created_at')

    context = {
        'student': student,
        'reports': reports_list,
        'evaluations': evaluations,
    }
    return render(request, 'supervisors/student_detail.html', context)


@login_required
@role_required('supervisor')
def report_review(request, pk=None):
    """Review a weekly report."""
    supervisor = get_object_or_404(SupervisorProfile, user=request.user)

    if pk:
        report = get_object_or_404(WeeklyReport, pk=pk, supervisor=supervisor)

        if request.method == 'POST':
            form = ReportReviewForm(request.POST)
            if form.is_valid():
                report.score = form.cleaned_data['score']
                report.feedback = form.cleaned_data['feedback']
                report.status = form.cleaned_data['status']
                report.reviewed_at = timezone.now()
                report.save()

                # Notify the student
                Notification.objects.create(
                    recipient=report.student.user,
                    notification_type='report',
                    title=f'Report Reviewed: Week {report.week_number}',
                    message=f'Your week {report.week_number} report has been {report.get_status_display().lower()}. Score: {report.score}/100',
                    link=f'/student/reports/',
                )
                messages.success(request, f'Report for Week {report.week_number} reviewed successfully!')
                return redirect('supervisors:report_review')
        else:
            form = ReportReviewForm()

        context = {'report': report, 'form': form}
        return render(request, 'supervisors/report_review.html', context)

    # List all pending reports
    pending_reports = WeeklyReport.objects.filter(
        supervisor=supervisor, status='submitted'
    ).select_related('student__user', 'internship').order_by('-created_at')

    reviewed_reports = WeeklyReport.objects.filter(
        supervisor=supervisor, status__in=['approved', 'rejected', 'reviewed']
    ).select_related('student__user', 'internship').order_by('-reviewed_at')[:20]

    context = {
        'pending_reports': pending_reports,
        'reviewed_reports': reviewed_reports,
    }
    return render(request, 'supervisors/report_review.html', context)


@login_required
@role_required('supervisor')
def evaluation(request, pk=None):
    """Create or view evaluations for students."""
    supervisor = get_object_or_404(SupervisorProfile, user=request.user)

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        internship_id = request.POST.get('internship_id')
        student = get_object_or_404(StudentProfile, pk=student_id)
        internship = get_object_or_404(Internship, pk=internship_id)

        form = EvaluationForm(request.POST)
        if form.is_valid():
            eval_obj = form.save(commit=False)
            eval_obj.supervisor = supervisor
            eval_obj.student = student
            eval_obj.internship = internship
            eval_obj.save()

            Notification.objects.create(
                recipient=student.user,
                notification_type='evaluation',
                title='New Evaluation Submitted',
                message=f'Your supervisor has submitted {"a final" if eval_obj.is_final else "an"} evaluation.',
                link='/student/reports/',
            )
            messages.success(request, 'Evaluation submitted successfully!')
            return redirect('supervisors:evaluation')
    else:
        form = EvaluationForm()

    # Get students assigned to this supervisor
    assigned_student_ids = WeeklyReport.objects.filter(
        supervisor=supervisor
    ).values_list('student_id', flat=True).distinct()
    students = StudentProfile.objects.filter(user_id__in=assigned_student_ids).select_related('user')

    evaluations = Evaluation.objects.filter(supervisor=supervisor).select_related(
        'student__user', 'internship'
    ).order_by('-created_at')

    context = {
        'form': form,
        'students': students,
        'evaluations': evaluations,
    }
    return render(request, 'supervisors/evaluation.html', context)


@login_required
@role_required('supervisor')
def settings(request):
    """Supervisor account settings."""
    supervisor = get_object_or_404(SupervisorProfile, user=request.user)

    if request.method == 'POST':
        form = SupervisorProfileForm(request.POST, instance=supervisor, user=request.user)
        if form.is_valid():
            form.save()
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.phone = form.cleaned_data['phone']
            if 'avatar' in request.FILES:
                request.user.avatar = request.FILES['avatar']
            request.user.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('supervisors:settings')
    else:
        form = SupervisorProfileForm(instance=supervisor, user=request.user)

    context = {'form': form, 'supervisor': supervisor}
    return render(request, 'supervisors/settings.html', context)
