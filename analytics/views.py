"""
============================================================
Analytics Views - Advanced Analytics & Insights Dashboard
============================================================
Provides rich, interactive analytics dashboards with role-specific
data visualizations powered by Chart.js. Includes application funnel,
skill demand trends, university leaderboard, and more.
============================================================
"""

import json
from collections import Counter

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Q, F
from django.utils import timezone
from datetime import timedelta

from internships.models import Internship, InternshipCategory
from applications.models import Application
from accounts.models import CustomUser, StudentProfile, CompanyProfile, SupervisorProfile
from reports.models import WeeklyReport, Evaluation
from interviews.models import Interview


@login_required
def dashboard(request):
    """Main analytics dashboard — routes to role-specific analytics."""
    role = request.user.role

    if role == 'student':
        return student_analytics(request)
    elif role == 'company':
        return company_analytics(request)
    elif role == 'supervisor':
        return supervisor_analytics(request)
    else:
        return admin_analytics(request)


@login_required
def admin_analytics(request):
    """Platform-wide analytics for administrators."""

    # ---- Summary Stats ----
    stats = {
        'total_users': CustomUser.objects.count(),
        'total_students': CustomUser.objects.filter(role=CustomUser.STUDENT).count(),
        'total_companies': CustomUser.objects.filter(role=CustomUser.COMPANY).count(),
        'total_supervisors': CustomUser.objects.filter(role=CustomUser.SUPERVISOR).count(),
        'total_internships': Internship.objects.count(),
        'open_positions': Internship.objects.filter(status='open', is_approved=True).count(),
        'total_applications': Application.objects.count(),
        'total_interviews': Interview.objects.count(),
        'accepted_offers': Application.objects.filter(status='accepted').count(),
        'avg_match_score': Application.objects.filter(ai_match_score__isnull=False).aggregate(
            avg=Avg('ai_match_score')
        )['avg'] or 0,
    }

    # ---- Application Funnel ----
    funnel_data = {
        'Pending': Application.objects.filter(status='pending').count(),
        'Reviewing': Application.objects.filter(status='reviewing').count(),
        'Assessment': Application.objects.filter(status='assessment').count(),
        'Interview': Application.objects.filter(status='interview').count(),
        'Offer': Application.objects.filter(status='offer').count(),
        'Accepted': Application.objects.filter(status='accepted').count(),
        'Rejected': Application.objects.filter(status='rejected').count(),
    }

    # ---- Internship by Category ----
    category_data = list(
        InternshipCategory.objects.filter(is_active=True).annotate(
            count=Count('internships')
        ).values('name', 'count').order_by('-count')[:10]
    )

    # ---- Top Skills Demand ----
    all_skills = []
    for internship in Internship.objects.exclude(skills_required='').values_list('skills_required', flat=True):
        skills = [s.strip().lower() for s in internship.split(',') if s.strip()]
        all_skills.extend(skills)
    skills_counter = Counter(all_skills)
    top_skills = skills_counter.most_common(10)

    # ---- Internship Type Distribution ----
    type_data = list(
        Internship.objects.values('internship_type').annotate(
            count=Count('id')
        ).order_by('-count')
    )

    # ---- Monthly Registrations (last 6 months) ----
    six_months_ago = timezone.now() - timedelta(days=180)
    monthly_registrations = []
    for i in range(6):
        start = timezone.now() - timedelta(days=(5 - i) * 30 + 30)
        end = timezone.now() - timedelta(days=(5 - i) * 30)
        count = CustomUser.objects.filter(date_joined__gte=start, date_joined__lt=end).count()
        monthly_registrations.append({
            'month': start.strftime('%b %Y'),
            'count': count,
        })

    # ---- Monthly Internship Postings (last 6 months) ----
    monthly_postings = []
    for i in range(6):
        start = timezone.now() - timedelta(days=(5 - i) * 30 + 30)
        end = timezone.now() - timedelta(days=(5 - i) * 30)
        count = Internship.objects.filter(created_at__gte=start, created_at__lt=end).count()
        monthly_postings.append({
            'month': start.strftime('%b %Y'),
            'count': count,
        })

    # ---- University Leaderboard ----
    university_data = list(
        StudentProfile.objects.exclude(university='').values('university').annotate(
            student_count=Count('user'),
            accepted_count=Count(
                'applications', filter=Q(applications__status='accepted')
            )
        ).order_by('-accepted_count')[:10]
    )

    # ---- AI Match Score Distribution ----
    score_ranges = [
        ('50-59', 50, 60), ('60-69', 60, 70), ('70-79', 70, 80),
        ('80-89', 80, 90), ('90-98', 90, 99),
    ]
    score_distribution = []
    for label, low, high in score_ranges:
        count = Application.objects.filter(
            ai_match_score__gte=low, ai_match_score__lt=high
        ).count()
        score_distribution.append({'range': label, 'count': count})

    context = {
        'stats': stats,
        'funnel_data': json.dumps(funnel_data),
        'category_data': json.dumps(category_data),
        'top_skills': json.dumps([{'skill': s, 'count': c} for s, c in top_skills]),
        'type_data': json.dumps(type_data),
        'monthly_registrations': json.dumps(monthly_registrations),
        'monthly_postings': json.dumps(monthly_postings),
        'university_data': json.dumps(university_data),
        'score_distribution': json.dumps(score_distribution),
        'analytics_role': 'admin',
    }
    return render(request, 'analytics/dashboard.html', context)


@login_required
def student_analytics(request):
    """Personal analytics for students."""
    profile = StudentProfile.objects.filter(user=request.user).first()
    if not profile:
        return render(request, 'analytics/dashboard.html', {'analytics_role': 'student', 'stats': {}})

    applications = Application.objects.filter(student=profile)

    # ---- Summary Stats ----
    stats = {
        'total_applications': applications.count(),
        'pending': applications.filter(status='pending').count(),
        'interviews': applications.filter(status='interview').count(),
        'accepted': applications.filter(status='accepted').count(),
        'rejected': applications.filter(status='rejected').count(),
        'avg_match_score': applications.filter(ai_match_score__isnull=False).aggregate(
            avg=Avg('ai_match_score')
        )['avg'] or 0,
        'total_reports': WeeklyReport.objects.filter(student=profile).count(),
        'avg_report_score': WeeklyReport.objects.filter(
            student=profile, score__isnull=False
        ).aggregate(avg=Avg('score'))['avg'] or 0,
    }

    # ---- Application Status Breakdown ----
    status_data = {}
    for status_key, status_label in Application.STATUS_CHOICES:
        count = applications.filter(status=status_key).count()
        if count > 0:
            status_data[status_label] = count

    # ---- Weekly Report Scores Over Time ----
    report_scores = list(
        WeeklyReport.objects.filter(
            student=profile, score__isnull=False
        ).order_by('week_number').values('week_number', 'score')
    )

    # ---- Applications Timeline (last 6 months) ----
    monthly_apps = []
    for i in range(6):
        start = timezone.now() - timedelta(days=(5 - i) * 30 + 30)
        end = timezone.now() - timedelta(days=(5 - i) * 30)
        count = applications.filter(applied_at__gte=start, applied_at__lt=end).count()
        monthly_apps.append({
            'month': start.strftime('%b %Y'),
            'count': count,
        })

    context = {
        'stats': stats,
        'status_data': json.dumps(status_data),
        'report_scores': json.dumps(report_scores),
        'monthly_apps': json.dumps(monthly_apps),
        'analytics_role': 'student',
    }
    return render(request, 'analytics/student_analytics.html', context)


@login_required
def company_analytics(request):
    """Recruitment analytics for companies."""
    company = CompanyProfile.objects.filter(user=request.user).first()
    if not company:
        return render(request, 'analytics/dashboard.html', {'analytics_role': 'company', 'stats': {}})

    internships = Internship.objects.filter(company=company)
    applications = Application.objects.filter(internship__company=company)

    # ---- Summary Stats ----
    stats = {
        'total_internships': internships.count(),
        'active_internships': internships.filter(status='open', is_approved=True).count(),
        'total_applications': applications.count(),
        'pending_review': applications.filter(status='pending').count(),
        'interviews_scheduled': Interview.objects.filter(
            application__internship__company=company, outcome='pending'
        ).count(),
        'offers_extended': applications.filter(status__in=['offer', 'accepted']).count(),
        'avg_match_score': applications.filter(ai_match_score__isnull=False).aggregate(
            avg=Avg('ai_match_score')
        )['avg'] or 0,
        'total_views': sum(internships.values_list('views_count', flat=True)),
    }

    # ---- Application Funnel for this company ----
    funnel_data = {}
    for status_key, status_label in Application.STATUS_CHOICES:
        count = applications.filter(status=status_key).count()
        funnel_data[status_label] = count

    # ---- Applications per Internship ----
    per_internship = list(
        internships.annotate(
            app_count=Count('applications')
        ).values('title', 'app_count').order_by('-app_count')[:10]
    )

    # ---- Monthly Applications Trend ----
    monthly_apps = []
    for i in range(6):
        start = timezone.now() - timedelta(days=(5 - i) * 30 + 30)
        end = timezone.now() - timedelta(days=(5 - i) * 30)
        count = applications.filter(applied_at__gte=start, applied_at__lt=end).count()
        monthly_apps.append({
            'month': start.strftime('%b %Y'),
            'count': count,
        })

    # ---- Top Candidate Match Scores ----
    top_candidates = list(
        applications.filter(ai_match_score__isnull=False).select_related(
            'student__user', 'internship'
        ).order_by('-ai_match_score').values(
            'student__user__first_name', 'student__user__last_name',
            'internship__title', 'ai_match_score'
        )[:10]
    )

    context = {
        'stats': stats,
        'funnel_data': json.dumps(funnel_data),
        'per_internship': json.dumps(per_internship),
        'monthly_apps': json.dumps(monthly_apps),
        'top_candidates': top_candidates,
        'analytics_role': 'company',
    }
    return render(request, 'analytics/company_analytics.html', context)


@login_required
def supervisor_analytics(request):
    """Supervision analytics for academic supervisors."""
    supervisor = SupervisorProfile.objects.filter(user=request.user).first()
    if not supervisor:
        return render(request, 'analytics/dashboard.html', {'analytics_role': 'supervisor', 'stats': {}})

    reports = WeeklyReport.objects.filter(supervisor=supervisor)
    evaluations = Evaluation.objects.filter(supervisor=supervisor)

    assigned_student_ids = reports.values_list('student_id', flat=True).distinct()

    stats = {
        'assigned_students': assigned_student_ids.count(),
        'total_reports_reviewed': reports.filter(status__in=['approved', 'reviewed']).count(),
        'pending_reports': reports.filter(status='submitted').count(),
        'total_evaluations': evaluations.count(),
        'avg_report_score': reports.filter(score__isnull=False).aggregate(
            avg=Avg('score')
        )['avg'] or 0,
        'avg_eval_score': evaluations.aggregate(
            avg=Avg('overall_score')
        )['avg'] or 0,
    }

    # ---- Report Status Breakdown ----
    report_status = {}
    for status_key, status_label in WeeklyReport.STATUS_CHOICES:
        count = reports.filter(status=status_key).count()
        if count > 0:
            report_status[status_label] = count

    # ---- Student Performance (avg report scores by student) ----
    student_performance = list(
        reports.filter(score__isnull=False).values(
            'student__user__first_name', 'student__user__last_name'
        ).annotate(
            avg_score=Avg('score'),
            reports_count=Count('id')
        ).order_by('-avg_score')[:10]
    )

    context = {
        'stats': stats,
        'report_status': json.dumps(report_status),
        'student_performance': json.dumps(student_performance),
        'analytics_role': 'supervisor',
    }
    return render(request, 'analytics/supervisor_analytics.html', context)
