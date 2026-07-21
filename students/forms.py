"""
============================================================
Students Forms - Profile & Report Forms
============================================================
"""

from django import forms
from accounts.models import StudentProfile, CustomUser
from reports.models import WeeklyReport


class StudentProfileForm(forms.ModelForm):
    """Form for editing student profile details."""
    first_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = StudentProfile
        fields = [
            'date_of_birth', 'gender', 'address', 'city', 'country',
            'university', 'department', 'student_id', 'education_level',
            'current_semester', 'gpa', 'expected_graduation',
            'skills', 'experience', 'languages',
            'linkedin_url', 'github_url', 'portfolio_url', 'bio',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'university': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
            'education_level': forms.Select(attrs={'class': 'form-select'}),
            'current_semester': forms.TextInput(attrs={'class': 'form-control'}),
            'gpa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'expected_graduation': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Python, JavaScript, React...'}),
            'experience': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'languages': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'English, Bangla...'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/...'}),
            'github_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/...'}),
            'portfolio_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['phone'].initial = user.phone


class WeeklyReportForm(forms.ModelForm):
    """Form for submitting weekly reports."""
    class Meta:
        model = WeeklyReport
        fields = ['internship', 'week_number', 'title', 'activities', 'challenges', 'next_week_plan', 'hours_worked']
        widgets = {
            'internship': forms.Select(attrs={'class': 'form-select'}),
            'week_number': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'activities': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'challenges': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'next_week_plan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'hours_worked': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
        }
