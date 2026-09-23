"""
============================================================
Administration Views - Admin Portal Operations
============================================================
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q, Sum, Avg
from django.utils import timezone
from datetime import datetime, timedelta

from accounts.decorators import role_required
from accounts.models import CustomUser, StudentProfile, CompanyProfile, SupervisorProfile
from internships.models import Internship, InternshipCategory
from applications.models import Application
from reports.models import WeeklyReport, Evaluation
from billing.models import Subscription, PaymentTransaction
from documents.models import ActivityLog
from notifications.models import Notification
from administration.forms import (
    UserEditForm, InternshipModerationForm,
    CompanyVerificationForm, InternshipCategoryForm
)



@login_required
@role_required('admin')
def dashboard(request):
    """Admin dashboard with system-wide analytics."""
    stats = {
        'total_users': CustomUser.objects.count(),
        'total_students': CustomUser.objects.filter(role=CustomUser.STUDENT).count(),
        'total_companies': CustomUser.objects.filter(role=CustomUser.COMPANY).count(),
        'total_supervisors': CustomUser.objects.filter(role=CustomUser.SUPERVISOR).count(),
        'total_internships': Internship.objects.count(),
        'pending_internships': Internship.objects.filter(is_approved=False).count(),
        'total_applications': Application.objects.count(),
        'unverified_companies': CompanyProfile.objects.filter(is_verified=False).count(),
    }

    recent_users = CustomUser.objects.order_by('-date_joined')[:5]
    recent_activities = ActivityLog.objects.select_related('user').order_by('-created_at')[:10]
    pending_moderation = Internship.objects.filter(is_approved=False).select_related('company')[:5]

    context = {
        'stats': stats,
        'recent_users': recent_users,
        'recent_activities': recent_activities,
        'pending_moderation': pending_moderation,
    }
    return render(request, 'administration/dashboard.html', context)


@login_required
@role_required('admin')
def user_management(request):
    """List and manage all platform users with role tabs, search, and suspension filters."""
    role_filter = request.GET.get('role', '')
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('q', '')

    users = CustomUser.objects.all().order_by('-date_joined')

    user_counts = {
        'all': CustomUser.objects.count(),
        'student': CustomUser.objects.filter(role=CustomUser.STUDENT).count(),
        'company': CustomUser.objects.filter(role=CustomUser.COMPANY).count(),
        'supervisor': CustomUser.objects.filter(role=CustomUser.SUPERVISOR).count(),
        'admin': CustomUser.objects.filter(role=CustomUser.ADMIN).count(),
        'suspended': CustomUser.objects.filter(is_active=False).count(),
    }

    if role_filter:
        users = users.filter(role=role_filter)
    if status_filter == 'suspended':
        users = users.filter(is_active=False)
    elif status_filter == 'active':
        users = users.filter(is_active=True)

    if search_query:
        users = users.filter(
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(username__icontains=search_query)
        )

    context = {
        'users': users,
        'role_filter': role_filter,
        'status_filter': status_filter,
        'search_query': search_query,
        'user_counts': user_counts,
    }
    return render(request, 'administration/user_management.html', context)


@login_required
@role_required('admin')
def user_detail(request, pk=None):
    """View and edit user details with complete admin observation audit trail."""
    user_obj = get_object_or_404(CustomUser, pk=pk)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'User account for {user_obj.email} updated successfully.')
            return redirect('administration:user_detail', pk=pk)
    else:
        form = UserEditForm(instance=user_obj)

    # Admin observation context data
    observation_data = {}
    if user_obj.is_student and hasattr(user_obj, 'student_profile'):
        observation_data['student_profile'] = user_obj.student_profile
        observation_data['applications'] = Application.objects.filter(student=user_obj.student_profile).select_related('internship__company').order_by('-applied_at')
        observation_data['reports'] = WeeklyReport.objects.filter(student=user_obj.student_profile).order_by('-week_number')
    elif user_obj.is_company and hasattr(user_obj, 'company_profile'):
        observation_data['company_profile'] = user_obj.company_profile
        observation_data['internships'] = Internship.objects.filter(company=user_obj.company_profile).order_by('-created_at')
    elif user_obj.is_supervisor and hasattr(user_obj, 'supervisor_profile'):
        observation_data['supervisor_profile'] = user_obj.supervisor_profile
        observation_data['assigned_reports'] = WeeklyReport.objects.filter(supervisor=user_obj.supervisor_profile).order_by('-created_at')

    from billing.models import Subscription
    observation_data['active_subscription'] = Subscription.objects.filter(user=user_obj, is_active=True).order_by('-started_at').first()
    observation_data['user_activities'] = ActivityLog.objects.filter(user=user_obj).order_by('-created_at')[:15]

    context = {
        'target_user': user_obj,
        'form': form,
        'obs': observation_data,
    }
    return render(request, 'administration/user_detail.html', context)


@login_required
@role_required('admin')
def user_cancel_subscription(request, pk=None):
    """Cancel / revoke active subscription for a user (Student or Company) with explicit violation reason."""
    user_obj = get_object_or_404(CustomUser, pk=pk)
    from billing.models import Subscription
    from notifications.models import Notification

    reason = request.GET.get('reason', '').strip() or request.POST.get('reason', '').strip() or "Administrative Policy Compliance Review"

    active_subs = Subscription.objects.filter(user=user_obj, is_active=True)
    count = active_subs.count()

    plan_names = ", ".join(sub.plan_display_name for sub in active_subs) if count > 0 else "Active Package"
    active_subs.update(is_active=False)

    if user_obj.is_company and hasattr(user_obj, 'company_profile'):
        user_obj.company_profile.subscription_plan = 'basic'
        user_obj.company_profile.save()

    # Notify the Company or Student user with clean plain text message & direct link to Support page
    if count > 0:
        Notification.objects.create(
            recipient=user_obj,
            notification_type='system',
            title='⚠️ Subscription Package Revoked',
            message=f'Your subscription package ({plan_names}) was revoked by an administrator. Reason: {reason}. Click "View Page" to read platform rules and contact support.',
            link=f'/accounts/suspended/?type=revocation&reason={reason}',
            priority='high',
        )

    messages.success(request, f'Successfully revoked {count} active subscription(s) for user {user_obj.email}. Account reverted to Basic Free tier & notification sent.')
    return redirect('administration:user_detail', pk=pk)


@login_required
@role_required('admin')
def user_suspend(request, pk=None):
    """Suspend or reactivate any user account (Student, Supervisor, Company, Admin)."""
    user_obj = get_object_or_404(CustomUser, pk=pk)
    if user_obj == request.user:
        messages.error(request, 'You cannot suspend your own admin account.')
        return redirect('administration:user_management')

    user_obj.is_active = not user_obj.is_active
    user_obj.save()

    status_text = 'reactivated' if user_obj.is_active else 'suspended'
    messages.warning(request, f'User account ({user_obj.email}) has been {status_text}.')
    return redirect(request.META.get('HTTP_REFERER', 'administration:user_management'))


@login_required
@role_required('admin')
def user_delete(request, pk=None):
    """Permanently delete any user account and associated profile."""
    user_obj = get_object_or_404(CustomUser, pk=pk)
    if user_obj == request.user:
        messages.error(request, 'You cannot delete your own admin account.')
        return redirect('administration:user_management')

    email = user_obj.email
    user_obj.delete()
    messages.success(request, f'User account {email} has been permanently deleted.')
    return redirect('administration:user_management')



@login_required
@role_required('admin')
def internship_moderation(request):
    """Moderate internship listings (approve/reject)."""
    if request.method == 'POST':
        internship_id = request.POST.get('internship_id')
        internship = get_object_or_404(Internship, pk=internship_id)
        action = request.POST.get('action')

        if action == 'approve':
            internship.is_approved = True
            if internship.status == 'draft':
                internship.status = 'open'
            internship.save()

            Notification.objects.create(
                recipient=internship.company.user,
                notification_type='internship',
                title='Internship Approved',
                message=f'Your internship listing "{internship.title}" has been approved and is now live!',
                link=f'/company/internship-list/',
            )
            messages.success(request, f'Internship "{internship.title}" approved.')
        elif action == 'reject':
            internship.is_approved = False
            internship.status = 'cancelled'
            internship.save()

            Notification.objects.create(
                recipient=internship.company.user,
                notification_type='internship',
                title='Internship Rejected',
                message=f'Your internship listing "{internship.title}" was not approved.',
                link=f'/company/internship-list/',
            )
            messages.warning(request, f'Internship "{internship.title}" rejected.')

        return redirect('administration:internship_moderation')

    pending_list = Internship.objects.filter(is_approved=False).select_related('company')
    approved_list = Internship.objects.filter(is_approved=True).select_related('company')[:20]

    context = {
        'pending_list': pending_list,
        'approved_list': approved_list,
    }
    return render(request, 'administration/internship_moderation.html', context)


@login_required
@role_required('admin')
def internship_preview(request, pk=None):
    """Preview internship details for admin moderation."""
    internship = get_object_or_404(Internship, pk=pk)
    context = {'internship': internship}
    return render(request, 'administration/internship_preview.html', context)


@login_required
@role_required('admin')
def admin_internship_edit(request, pk=None):
    """Admin edit internship post details."""
    from companies.forms import InternshipForm
    internship = get_object_or_404(Internship, pk=pk)

    if request.method == 'POST':
        form = InternshipForm(request.POST, instance=internship)
        if form.is_valid():
            form.save()
            messages.success(request, f'Internship post "{internship.title}" updated by admin.')
            return redirect('administration:internship_moderation')
    else:
        form = InternshipForm(instance=internship)

    context = {'form': form, 'internship': internship}
    return render(request, 'administration/internship_edit.html', context)


@login_required
@role_required('admin')
def internship_unpublish(request, pk=None):
    """Unpublish an approved internship listing."""
    internship = get_object_or_404(Internship, pk=pk)
    if request.method == 'POST':
        internship.is_approved = False
        internship.status = 'draft'
        internship.save()

        Notification.objects.create(
            recipient=internship.company.user,
            notification_type='internship',
            title='Internship Listing Unpublished',
            message=f'Your internship listing "{internship.title}" has been unpublished by administration.',
            link='/company/internship-list/',
        )
        messages.warning(request, f'Internship "{internship.title}" has been unpublished.')
    return redirect('administration:internship_moderation')


@login_required
@role_required('admin')
def company_management(request):
    """Verify, suspend and manage company accounts."""
    if request.method == 'POST':
        company_id = request.POST.get('company_id')
        action = request.POST.get('action')
        company = get_object_or_404(CompanyProfile, pk=company_id)

        if action == 'suspend':
            company.user.is_active = not company.user.is_active
            company.user.save()
            status_text = 'active' if company.user.is_active else 'suspended'
            messages.warning(request, f'Company "{company.company_name}" user account status set to {status_text}.')
        else:
            company.is_verified = not company.is_verified
            company.save()

            status_text = 'verified' if company.is_verified else 'unverified'
            Notification.objects.create(
                recipient=company.user,
                notification_type='system',
                title='Company Verification Update',
                message=f'Your company profile status is now: {status_text}.',
                link='/company/profile/',
            )
            messages.success(request, f'Company "{company.company_name}" marked as {status_text}.')
        return redirect('administration:company_management')

    companies = CompanyProfile.objects.select_related('user').order_by('-created_at')
    context = {'companies': companies}
    return render(request, 'administration/company_management.html', context)


@login_required
@role_required('admin')
def activity_logs(request):
    """View system activity logs."""
    logs = ActivityLog.objects.select_related('user').order_by('-created_at')[:100]
    context = {'logs': logs}
    return render(request, 'administration/activity_logs.html', context)


@login_required
@role_required('admin')
def platform_settings(request):
    """Platform settings and category management."""
    if request.method == 'POST':
        form = InternshipCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" added successfully.')
            return redirect('administration:platform_settings')
    else:
        form = InternshipCategoryForm()

    categories = InternshipCategory.objects.all()
    context = {
        'categories': categories,
        'form': form,
    }
    return render(request, 'administration/platform_settings.html', context)


def _get_report_data(request):
    """
    Core data engine for Admin Reporting & Exporting.
    Extracts query parameters, computes date filters, queries models,
    applies filters and sorting, and returns structured report data context.
    """
    report_type = request.GET.get('report_type', 'summary')
    date_preset = request.GET.get('date_preset', '30days')
    start_date_str = request.GET.get('start_date', '')
    end_date_str = request.GET.get('end_date', '')
    company_id = request.GET.get('company_id', '')
    status_filter = request.GET.get('status', '')
    payment_method = request.GET.get('payment_method', '')
    plan_category = request.GET.get('plan_category', '')
    sort_by = request.GET.get('sort_by', 'date')
    order = request.GET.get('order', 'desc')
    search_q = request.GET.get('q', '').strip()

    now = timezone.now()
    start_date = None
    end_date = None

    if date_preset == 'today':
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = now
    elif date_preset == '7days':
        start_date = now - timedelta(days=7)
        end_date = now
    elif date_preset == '30days':
        start_date = now - timedelta(days=30)
        end_date = now
    elif date_preset == '1year':
        start_date = now - timedelta(days=365)
        end_date = now
    elif date_preset == 'custom' and start_date_str:
        try:
            sd = datetime.strptime(start_date_str, '%Y-%m-%d')
            start_date = timezone.make_aware(sd)
            if end_date_str:
                ed = datetime.strptime(end_date_str, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
                end_date = timezone.make_aware(ed)
            else:
                end_date = now
        except ValueError:
            start_date = now - timedelta(days=30)
            end_date = now
    else:  # 'all' or default
        date_preset = 'all'
        start_date = None
        end_date = None

    order_prefix = '-' if order == 'desc' else ''

    context = {
        'report_type': report_type,
        'date_preset': date_preset,
        'start_date_str': start_date_str,
        'end_date_str': end_date_str,
        'company_id': company_id,
        'status_filter': status_filter,
        'payment_method': payment_method,
        'plan_category': plan_category,
        'sort_by': sort_by,
        'order': order,
        'search_q': search_q,
        'all_companies': CompanyProfile.objects.select_related('user').order_by('company_name'),
        'generated_at': now,
        'start_date': start_date,
        'end_date': end_date,
    }

    # 1. SUMMARY REPORT
    if report_type == 'summary':
        users_qs = CustomUser.objects.all()
        internships_qs = Internship.objects.all()
        apps_qs = Application.objects.all()
        txns_qs = PaymentTransaction.objects.all()
        subs_qs = Subscription.objects.all()

        if start_date:
            users_qs = users_qs.filter(date_joined__gte=start_date)
            internships_qs = internships_qs.filter(created_at__gte=start_date)
            apps_qs = apps_qs.filter(applied_at__gte=start_date)
            txns_qs = txns_qs.filter(created_at__gte=start_date)
            subs_qs = subs_qs.filter(created_at__gte=start_date)
        if end_date:
            users_qs = users_qs.filter(date_joined__lte=end_date)
            internships_qs = internships_qs.filter(created_at__lte=end_date)
            apps_qs = apps_qs.filter(applied_at__lte=end_date)
            txns_qs = txns_qs.filter(created_at__lte=end_date)
            subs_qs = subs_qs.filter(created_at__lte=end_date)

        total_rev = txns_qs.filter(status='completed').aggregate(total=Sum('amount'))['total'] or 0

        context['summary_metrics'] = {
            'total_users': users_qs.count(),
            'students_count': users_qs.filter(role='student').count(),
            'companies_count': users_qs.filter(role='company').count(),
            'supervisors_count': users_qs.filter(role='supervisor').count(),
            'internships_count': internships_qs.count(),
            'approved_internships': internships_qs.filter(is_approved=True).count(),
            'applications_count': apps_qs.count(),
            'placed_students': apps_qs.filter(status='accepted').count(),
            'total_revenue': total_rev,
            'completed_txns': txns_qs.filter(status='completed').count(),
            'active_subscriptions': subs_qs.filter(is_active=True).count(),
        }

        recent_txns = txns_qs.select_related('user', 'subscription').order_by('-created_at')[:10]
        recent_apps = apps_qs.select_related('student__user', 'internship__company').order_by('-applied_at')[:10]
        context['recent_txns'] = recent_txns
        context['recent_apps'] = recent_apps

    # 2. APPLICATIONS & PLACEMENTS REPORT
    elif report_type == 'applications':
        qs = Application.objects.select_related('student__user', 'internship__company')

        if start_date:
            qs = qs.filter(applied_at__gte=start_date)
        if end_date:
            qs = qs.filter(applied_at__lte=end_date)
        if company_id:
            qs = qs.filter(internship__company_id=company_id)
        if status_filter:
            qs = qs.filter(status=status_filter)

        if search_q:
            qs = qs.filter(
                Q(student__user__first_name__icontains=search_q) |
                Q(student__user__last_name__icontains=search_q) |
                Q(student__user__email__icontains=search_q) |
                Q(internship__title__icontains=search_q) |
                Q(internship__company__company_name__icontains=search_q)
            )

        if sort_by == 'company':
            sort_field = f"{order_prefix}internship__company__company_name"
        elif sort_by == 'student':
            sort_field = f"{order_prefix}student__user__first_name"
        elif sort_by == 'status':
            sort_field = f"{order_prefix}status"
        elif sort_by == 'score':
            sort_field = f"{order_prefix}ai_match_score"
        else:
            sort_field = f"{order_prefix}applied_at"

        qs = qs.order_by(sort_field)

        placed_count = qs.filter(status='accepted').count()
        total_count = qs.count()
        interview_count = qs.filter(status='interview').count()
        rejected_count = qs.filter(status='rejected').count()
        avg_score = qs.filter(ai_match_score__isnull=False).aggregate(avg=Avg('ai_match_score'))['avg'] or 0

        context['report_items'] = qs
        context['metrics'] = {
            'total_applications': total_count,
            'placed_count': placed_count,
            'interview_count': interview_count,
            'rejected_count': rejected_count,
            'avg_score': round(avg_score, 1),
        }

    # 3. SALES & FINANCIAL REVENUE REPORT
    elif report_type == 'sales':
        qs = PaymentTransaction.objects.select_related('user', 'subscription')

        if start_date:
            qs = qs.filter(created_at__gte=start_date)
        if end_date:
            qs = qs.filter(created_at__lte=end_date)
        if payment_method:
            qs = qs.filter(payment_method=payment_method)
        if status_filter:
            qs = qs.filter(status=status_filter)
        if plan_category:
            qs = qs.filter(subscription__plan_category=plan_category)

        if search_q:
            qs = qs.filter(
                Q(transaction_id__icontains=search_q) |
                Q(user__email__icontains=search_q) |
                Q(user__first_name__icontains=search_q) |
                Q(user__last_name__icontains=search_q) |
                Q(account_number__icontains=search_q)
            )

        if sort_by == 'amount':
            sort_field = f"{order_prefix}amount"
        elif sort_by == 'user':
            sort_field = f"{order_prefix}user__email"
        elif sort_by == 'method':
            sort_field = f"{order_prefix}payment_method"
        else:
            sort_field = f"{order_prefix}created_at"

        qs = qs.order_by(sort_field)

        total_rev = qs.filter(status='completed').aggregate(total=Sum('amount'))['total'] or 0
        completed_count = qs.filter(status='completed').count()
        pending_count = qs.filter(status='pending').count()
        bkash_total = qs.filter(status='completed', payment_method='bkash').aggregate(t=Sum('amount'))['t'] or 0
        nagad_total = qs.filter(status='completed', payment_method='nagad').aggregate(t=Sum('amount'))['t'] or 0
        card_total = qs.filter(status='completed', payment_method='card').aggregate(t=Sum('amount'))['t'] or 0

        context['report_items'] = qs
        context['metrics'] = {
            'total_revenue': total_rev,
            'completed_count': completed_count,
            'pending_count': pending_count,
            'bkash_total': bkash_total,
            'nagad_total': nagad_total,
            'card_total': card_total,
        }

    # 4. COMPANIES & PLACEMENTS ALLOCATION REPORT
    elif report_type == 'companies':
        companies = CompanyProfile.objects.select_related('user')
        if search_q:
            companies = companies.filter(
                Q(company_name__icontains=search_q) |
                Q(industry__icontains=search_q) |
                Q(user__email__icontains=search_q)
            )

        company_reports = []
        for comp in companies:
            internships = Internship.objects.filter(company=comp)
            apps = Application.objects.filter(internship__company=comp).select_related('student__user')

            if start_date:
                internships = internships.filter(created_at__gte=start_date)
                apps = apps.filter(applied_at__gte=start_date)
            if end_date:
                internships = internships.filter(created_at__lte=end_date)
                apps = apps.filter(applied_at__lte=end_date)

            placed_apps = apps.filter(status='accepted')

            company_reports.append({
                'company': comp,
                'internships_count': internships.count(),
                'applications_count': apps.count(),
                'placed_count': placed_apps.count(),
                'placed_students': placed_apps,
            })

        reverse = (order == 'desc')
        if sort_by == 'posted':
            company_reports.sort(key=lambda x: x['internships_count'], reverse=reverse)
        elif sort_by == 'placed':
            company_reports.sort(key=lambda x: x['placed_count'], reverse=reverse)
        elif sort_by == 'apps':
            company_reports.sort(key=lambda x: x['applications_count'], reverse=reverse)
        else:
            company_reports.sort(key=lambda x: x['company'].company_name.lower(), reverse=reverse)

        total_placed = sum(item['placed_count'] for item in company_reports)
        total_posted = sum(item['internships_count'] for item in company_reports)
        total_apps = sum(item['applications_count'] for item in company_reports)

        context['company_reports'] = company_reports
        context['metrics'] = {
            'total_companies': len(company_reports),
            'total_posted': total_posted,
            'total_apps': total_apps,
            'total_placed': total_placed,
        }

    # 5. STUDENTS ACTIVITY & SUPERVISION REPORT
    elif report_type == 'students':
        students = StudentProfile.objects.select_related('user', 'supervisor__user')
        if search_q:
            students = students.filter(
                Q(user__first_name__icontains=search_q) |
                Q(user__last_name__icontains=search_q) |
                Q(user__email__icontains=search_q) |
                Q(university__icontains=search_q) |
                Q(major__icontains=search_q)
            )

        student_reports = []
        for std in students:
            apps = Application.objects.filter(student=std)
            reports = WeeklyReport.objects.filter(student=std)

            if start_date:
                apps = apps.filter(applied_at__gte=start_date)
                reports = reports.filter(created_at__gte=start_date)
            if end_date:
                apps = apps.filter(applied_at__lte=end_date)
                reports = reports.filter(created_at__lte=end_date)

            placed_app = apps.filter(status='accepted').first()
            avg_report_score = reports.filter(score__isnull=False).aggregate(avg=Avg('score'))['avg'] or 0

            student_reports.append({
                'student': std,
                'apps_count': apps.count(),
                'placed_app': placed_app,
                'reports_count': reports.count(),
                'avg_score': round(avg_report_score, 1),
            })

        reverse = (order == 'desc')
        if sort_by == 'reports':
            student_reports.sort(key=lambda x: x['reports_count'], reverse=reverse)
        elif sort_by == 'score':
            student_reports.sort(key=lambda x: x['avg_score'], reverse=reverse)
        elif sort_by == 'apps':
            student_reports.sort(key=lambda x: x['apps_count'], reverse=reverse)
        else:
            student_reports.sort(key=lambda x: (x['student'].user.first_name or x['student'].user.email).lower(), reverse=reverse)

        context['student_reports'] = student_reports
        context['metrics'] = {
            'total_students': len(student_reports),
            'total_placed': sum(1 for item in student_reports if item['placed_app']),
            'total_reports': sum(item['reports_count'] for item in student_reports),
        }

    return context


@login_required
@role_required('admin')
def admin_reports(request):
    """Admin report generator interface view."""
    context = _get_report_data(request)
    return render(request, 'administration/reports.html', context)


@login_required
@role_required('admin')
def admin_reports_print(request):
    """Printable official admin report view (opens formatted print layout / triggers print)."""
    context = _get_report_data(request)
    context['is_print_mode'] = True
    return render(request, 'administration/reports_print.html', context)

