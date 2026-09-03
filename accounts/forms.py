"""
============================================================
Accounts Forms - Authentication & Registration
============================================================
Forms for user login, registration (Student, Company, Supervisor),
password management, and profile editing.
============================================================
"""

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.safestring import mark_safe
from accounts.models import CustomUser, StudentProfile, CompanyProfile, SupervisorProfile


class LoginForm(forms.Form):
    """Form for user login with email and password."""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'enter your email',
            'id': 'email',
        }),
        label='Email Address',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '••••••••',
            'id': 'password',
        }),
        label='Password',
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if email and password:
            user = authenticate(username=email, password=password)
            if user is None:
                # Check if the user exists and password is correct, but account is deactivated/suspended
                existing_user = CustomUser.objects.filter(email__iexact=email).first()
                if existing_user and existing_user.check_password(password) and not existing_user.is_active:
                    raise forms.ValidationError(
                        mark_safe(
                            'Your account has been suspended by administration. '
                            'Please visit our <a href="/accounts/suspended/" class="alert-link text-decoration-underline fw-bold">Support Page</a> to request account reinstatement.'
                        )
                    )
                raise forms.ValidationError('Invalid email or password.')
            if not user.is_active:
                raise forms.ValidationError(
                    mark_safe(
                        'Your account has been suspended by administration. '
                        'Please visit our <a href="/accounts/suspended/" class="alert-link text-decoration-underline fw-bold">Support Page</a> to request account reinstatement.'
                    )
                )
            cleaned_data['user'] = user
        return cleaned_data


class StudentRegistrationForm(forms.Form):
    """Registration form for Student users."""
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name',
            'id': 'first_name',
        }),
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name',
            'id': 'last_name',
        }),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com',
            'id': 'email',
        }),
    )
    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Minimum 8 characters',
            'id': 'password',
        }),
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Re-enter your password',
            'id': 'confirm_password',
        }),
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')
        return cleaned_data

    def save(self):
        data = self.cleaned_data
        username = data['email'].split('@')[0]
        # Ensure unique username
        base_username = username
        counter = 1
        while CustomUser.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = CustomUser.objects.create_user(
            email=data['email'],
            username=username,
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role=CustomUser.STUDENT,
        )
        # Create student profile
        StudentProfile.objects.create(user=user)
        return user


class CompanyRegistrationForm(forms.Form):
    """Registration form for Company/HR users."""
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contact person first name',
            'id': 'first_name',
        }),
        label='Contact First Name',
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contact person last name',
            'id': 'last_name',
        }),
        label='Contact Last Name',
    )
    company_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your company name',
            'id': 'company_name',
        }),
        label='Company Name',
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'company@example.com',
            'id': 'email',
        }),
        label='Business Email',
    )
    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Minimum 8 characters',
            'id': 'password',
        }),
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Re-enter your password',
            'id': 'confirm_password',
        }),
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')
        return cleaned_data

    def save(self):
        data = self.cleaned_data
        username = data['email'].split('@')[0]
        base_username = username
        counter = 1
        while CustomUser.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = CustomUser.objects.create_user(
            email=data['email'],
            username=username,
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role=CustomUser.COMPANY,
        )
        # Create company profile
        CompanyProfile.objects.create(
            user=user,
            company_name=data['company_name'],
            contact_person=f"{data['first_name']} {data['last_name']}",
            contact_email=data['email'],
        )
        return user


class SupervisorRegistrationForm(forms.Form):
    """Registration form for Academic Supervisor users."""
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name',
            'id': 'first_name',
        }),
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name',
            'id': 'last_name',
        }),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'university.email@edu.com',
            'id': 'email',
        }),
        label='University Email',
    )
    university = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'University name',
            'id': 'university',
        }),
    )
    department = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Department name',
            'id': 'department',
        }),
    )
    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Minimum 8 characters',
            'id': 'password',
        }),
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Re-enter your password',
            'id': 'confirm_password',
        }),
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')
        return cleaned_data

    def save(self):
        data = self.cleaned_data
        username = data['email'].split('@')[0]
        base_username = username
        counter = 1
        while CustomUser.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = CustomUser.objects.create_user(
            email=data['email'],
            username=username,
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role=CustomUser.SUPERVISOR,
        )
        # Create supervisor profile
        SupervisorProfile.objects.create(
            user=user,
            university=data['university'],
            department=data['department'],
        )
        return user


class ForgotPasswordForm(forms.Form):
    """Form for requesting a password reset email."""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your registered email',
            'id': 'email',
        }),
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('No account found with this email address.')
        return email
