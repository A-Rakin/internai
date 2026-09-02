"""
============================================================
Administration Views - Admin Portal Operations
============================================================
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q

from accounts.decorators import role_required
from accounts.models import CustomUser, StudentProfile, CompanyProfile, SupervisorProfile
from internships.models import Internship, InternshipCategory
from applications.models import Application
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
    """List and manage all platform users."""
    role_filter = request.GET.get('role', '')
    search_query = request.GET.get('q', '')

    users = CustomUser.objects.all().order_by('-date_joined')
    if role_filter:
        users = users.filter(role=role_filter)
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
        'search_query': search_query,
    }
    return render(request, 'administration/user_management.html', context)


@login_required
@role_required('admin')
def user_detail(request, pk=None):
    """View and edit user details."""
    user_obj = get_object_or_404(CustomUser, pk=pk)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'User account for {user_obj.email} updated successfully.')
            return redirect('administration:user_detail', pk=pk)
    else:
        form = UserEditForm(instance=user_obj)

    context = {
        'target_user': user_obj,
        'form': form,
    }
    return render(request, 'administration/user_detail.html', context)


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
