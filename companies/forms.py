"""
============================================================
Companies Forms - Profile, Internship & Interview Forms
============================================================
"""

from django import forms
from accounts.models import CompanyProfile
from internships.models import Internship, InternshipCategory
from interviews.models import Interview
from applications.models import Application


class CompanyProfileForm(forms.ModelForm):
    """Form for editing company profile details."""
    first_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CompanyProfile
        fields = [
            'company_name', 'logo', 'industry', 'company_size',
            'description', 'website', 'address', 'city', 'country',
            'contact_person', 'contact_email', 'contact_phone',
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'industry': forms.Select(attrs={'class': 'form-select'}),
            'company_size': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['phone'].initial = user.phone


class InternshipForm(forms.ModelForm):
    """Form for creating/editing internship listings."""
    class Meta:
        model = Internship
        fields = [
            'title', 'category', 'description', 'requirements',
            'skills_required', 'internship_type', 'location',
            'duration', 'stipend', 'positions', 'deadline', 'start_date',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'skills_required': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Python, Django, React...'}),
            'internship_type': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 3 months'}),
            'stipend': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'positions': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class InterviewScheduleForm(forms.ModelForm):
    """Form for scheduling interviews."""
    class Meta:
        model = Interview
        fields = [
            'interview_type', 'mode', 'scheduled_at', 'duration_minutes',
            'meeting_link', 'location', 'interviewer_name',
        ]
        widgets = {
            'interview_type': forms.Select(attrs={'class': 'form-select'}),
            'mode': forms.Select(attrs={'class': 'form-select'}),
            'scheduled_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control', 'min': 15}),
            'meeting_link': forms.URLInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'interviewer_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ApplicationStatusForm(forms.Form):
    """Form for updating application status and notes."""
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('reviewing', 'Under Review'),
        ('assessment', 'Assessment'),
        ('interview', 'Interview'),
        ('offer', 'Offer Extended'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    company_notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    rejection_reason = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}))
