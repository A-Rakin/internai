"""
============================================================
Supervisors Forms - Profile, Review & Evaluation Forms
============================================================
"""

from django import forms
from accounts.models import SupervisorProfile
from reports.models import WeeklyReport, Evaluation


class SupervisorProfileForm(forms.ModelForm):
    """Form for editing supervisor profile details."""
    first_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = SupervisorProfile
        fields = [
            'university', 'department', 'designation', 'employee_id',
            'expertise', 'max_students', 'bio',
        ]
        widgets = {
            'university': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'designation': forms.Select(attrs={'class': 'form-select'}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'expertise': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Machine Learning, Data Science...'}),
            'max_students': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['phone'].initial = user.phone


class ReportReviewForm(forms.Form):
    """Form for reviewing and scoring student reports."""
    score = forms.IntegerField(
        min_value=0, max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Score (0-100)'}),
    )
    feedback = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter your feedback...'}),
    )
    status = forms.ChoiceField(
        choices=[('approved', 'Approve'), ('rejected', 'Reject / Request Revision')],
        widget=forms.Select(attrs={'class': 'form-select'}),
    )


class EvaluationForm(forms.ModelForm):
    """Form for creating/editing student evaluations."""
    class Meta:
        model = Evaluation
        fields = [
            'technical_score', 'communication_score', 'professionalism_score',
            'attendance_score', 'overall_score', 'comments', 'recommendation', 'is_final',
        ]
        widgets = {
            'technical_score': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
            'communication_score': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
            'professionalism_score': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
            'attendance_score': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
            'overall_score': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'recommendation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_final': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
