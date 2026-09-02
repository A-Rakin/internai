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
            'logo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/png, image/jpeg, image/jpg, image/webp'}),
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
            'stipend': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'positions': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean_stipend(self):
        stipend = self.cleaned_data.get('stipend')
        if stipend is not None and stipend < 0:
            raise forms.ValidationError('Stipend cannot be negative. Enter 0 or a positive value.')
        return stipend

    def clean_positions(self):
        positions = self.cleaned_data.get('positions')
        if positions is not None and positions < 1:
            raise forms.ValidationError('Positions available must be at least 1.')
        return positions


class InterviewScheduleForm(forms.ModelForm):
    """Form for scheduling interviews with collision and sequential validation."""
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
            'meeting_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://meet.google.com/xyz...'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Office Room / Floor / Building'}),
            'interviewer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lead Interviewer Name'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        scheduled_at = cleaned_data.get('scheduled_at')
        duration = cleaned_data.get('duration_minutes') or 60
        interviewer = (cleaned_data.get('interviewer_name') or '').strip()

        from datetime import timedelta
        from django.utils import timezone

        if scheduled_at and scheduled_at < timezone.now():
            raise forms.ValidationError('Interview date and time cannot be in the past. Please select a future date and time.')

        # Check interviewer time collision
        if scheduled_at and interviewer:
            start_time = scheduled_at
            end_time = scheduled_at + timedelta(minutes=duration)

            conflicts = Interview.objects.filter(
                interviewer_name__iexact=interviewer,
                outcome__in=['pending', 'rescheduled']
            )
            if self.instance and self.instance.pk:
                conflicts = conflicts.exclude(pk=self.instance.pk)

            for conf in conflicts:
                conf_start = conf.scheduled_at
                conf_end = conf.scheduled_at + timedelta(minutes=conf.duration_minutes or 60)
                if conf_start < end_time and conf_end > start_time:
                    raise forms.ValidationError(
                        f"Interviewer collision: '{interviewer}' is already assigned to an interview on "
                        f"{conf.scheduled_at.strftime('%b %d, %Y at %I:%M %p')}. "
                        "The same interviewer cannot be assigned to overlapping interview slots. Please pick another time or interviewer."
                    )

        return cleaned_data


class InterviewEditForm(InterviewScheduleForm):
    """Form for editing/rescheduling existing interviews and updating outcomes."""
    class Meta(InterviewScheduleForm.Meta):
        fields = InterviewScheduleForm.Meta.fields + ['outcome', 'score', 'notes']
        widgets = dict(InterviewScheduleForm.Meta.widgets, **{
            'outcome': forms.Select(attrs={'class': 'form-select'}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100, 'placeholder': 'Score out of 100'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Interview evaluation notes and feedback...'}),
        })


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
