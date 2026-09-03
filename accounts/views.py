"""
============================================================
Accounts Views - Authentication & User Management
============================================================
Handles login, registration, logout, password management,
and role-based dashboard redirect for all user types.
============================================================
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings

from accounts.forms import (
    LoginForm,
    StudentRegistrationForm,
    CompanyRegistrationForm,
    SupervisorRegistrationForm,
    ForgotPasswordForm,
)
from accounts.models import CustomUser


def login_view(request):
    """Handle user login with email and password."""
    # Redirect authenticated users to their dashboard
    if request.user.is_authenticated:
        return redirect(request.user.get_dashboard_url())

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.email}!')
            # Redirect to the 'next' URL if provided, else dashboard
            next_url = request.GET.get('next', user.get_dashboard_url())
            return redirect(next_url)
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Log the user out and redirect to home page."""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('landing:home')


def register_student(request):
    """Handle student registration."""
    if request.user.is_authenticated:
        return redirect(request.user.get_dashboard_url())

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Student account created successfully! Welcome to InternAI.')
            return redirect('students:dashboard')
    else:
        form = StudentRegistrationForm()
    return render(request, 'accounts/register_student.html', {'form': form})


def register_company(request):
    """Handle company/HR registration."""
    if request.user.is_authenticated:
        return redirect(request.user.get_dashboard_url())

    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Company account created successfully! Welcome to InternAI.')
            return redirect('companies:dashboard')
    else:
        form = CompanyRegistrationForm()
    return render(request, 'accounts/register_company.html', {'form': form})


def register_supervisor(request):
    """Handle supervisor registration."""
    if request.user.is_authenticated:
        return redirect(request.user.get_dashboard_url())

    if request.method == 'POST':
        form = SupervisorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Supervisor account created successfully! Welcome to InternAI.')
            return redirect('supervisors:dashboard')
    else:
        form = SupervisorRegistrationForm()
    return render(request, 'accounts/register_supervisor.html', {'form': form})


def forgot_password(request):
    """Handle forgot password - send reset email."""
    if request.user.is_authenticated:
        return redirect(request.user.get_dashboard_url())

    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = CustomUser.objects.get(email=email)
            # Generate token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(
                f'/accounts/reset-password/?uid={uid}&token={token}'
            )
            # Send email (console backend in dev)
            send_mail(
                'InternAI - Password Reset',
                f'Click the link to reset your password: {reset_url}',
                'noreply@internai.com',
                [email],
                fail_silently=False,
            )
            messages.success(
                request,
                'Password reset link has been sent to your email. Check your terminal console for the link.'
            )
            return redirect('accounts:login')
    else:
        form = ForgotPasswordForm()
    return render(request, 'accounts/forgot_password.html', {'form': form})


def reset_password(request):
    """Handle password reset with token validation."""
    uid = request.GET.get('uid') or request.POST.get('uid')
    token = request.GET.get('token') or request.POST.get('token')

    if not uid or not token:
        messages.error(request, 'Invalid password reset link.')
        return redirect('accounts:forgot_password')

    try:
        user_id = force_str(urlsafe_base64_decode(uid))
        user = CustomUser.objects.get(pk=user_id)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        messages.error(request, 'Invalid password reset link.')
        return redirect('accounts:forgot_password')

    if not default_token_generator.check_token(user, token):
        messages.error(request, 'This password reset link has expired. Please request a new one.')
        return redirect('accounts:forgot_password')

    if request.method == 'POST':
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
        elif new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        else:
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Your password has been reset successfully. Please login.')
            return redirect('accounts:login')

    return render(request, 'accounts/reset_password.html', {'uid': uid, 'token': token})


@login_required
def change_password(request):
    """Handle password change for logged-in users."""
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not request.user.check_password(old_password):
            messages.error(request, 'Current password is incorrect.')
        elif len(new_password) < 8:
            messages.error(request, 'New password must be at least 8 characters long.')
        elif new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
        else:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Your password has been changed successfully.')
            return redirect(request.user.get_dashboard_url())

    return render(request, 'accounts/change_password.html')


@login_required
def dashboard_redirect(request):
    """Redirect authenticated users to their role-based dashboard."""
    return redirect(request.user.get_dashboard_url())


def suspended_support(request):
    """Render support request page for suspended users."""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        if email and message:
            try:
                from notifications.models import Notification
                from documents.models import ActivityLog
                
                user_obj = CustomUser.objects.filter(email__iexact=email).first()
                admin_users = CustomUser.objects.filter(role=CustomUser.ADMIN)

                for admin in admin_users:
                    Notification.objects.create(
                        recipient=admin,
                        notification_type='system',
                        title='Account Suspension Appeal',
                        message=f"Suspension appeal from {email}: {message[:120]}",
                        link='/admin-portal/user-management/',
                    )

                if user_obj:
                    ActivityLog.objects.create(
                        user=user_obj,
                        action="SUSPENSION_APPEAL",
                        description=f"User submitted suspension reinstatement request: {message[:150]}"
                    )
            except Exception as e:
                print(f"Error logging suspension appeal: {e}")

            messages.success(
                request,
                "Your reinstatement appeal has been submitted to system administration. "
                "Our team will review your request shortly."
            )
            return redirect('accounts:login')
        else:
            messages.error(request, "Please fill in all fields before submitting.")

    return render(request, 'accounts/suspended.html')

