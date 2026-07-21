"""
============================================================
Administration Forms - User & Platform Management Forms
============================================================
"""

from django import forms
from accounts.models import CustomUser
from internships.models import InternshipCategory


class UserEditForm(forms.Form):
    """Form for admin to edit user status."""
    is_active = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )


class InternshipModerationForm(forms.Form):
    """Form for approving/rejecting internship listings."""
    ACTION_CHOICES = [
        ('approve', 'Approve'),
        ('reject', 'Reject'),
    ]
    action = forms.ChoiceField(choices=ACTION_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))


class CompanyVerificationForm(forms.Form):
    """Form for verifying/unverifying companies."""
    is_verified = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))


class InternshipCategoryForm(forms.ModelForm):
    """Form for managing internship categories."""
    class Meta:
        model = InternshipCategory
        fields = ['name', 'description', 'icon', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'fas fa-code'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
