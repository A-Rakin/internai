"""
============================================================
Applications Models - Internship Applications
============================================================
Tracks student applications through the entire recruitment
pipeline from submission to acceptance/rejection.
============================================================
"""

from django.db import models
from accounts.models import StudentProfile
from internships.models import Internship


class Application(models.Model):
    """
    Internship application submitted by a student.
    
    Tracks the entire application lifecycle through multiple
    stages: Pending → Assessment → Interview → Offer → Accepted/Rejected.
    """

    # ---- Status Pipeline Choices ----
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),           # Just submitted
        ('reviewing', 'Under Review'),           # Being reviewed by company
        ('assessment', 'Assessment'),            # Technical assessment stage
        ('interview', 'Interview'),              # Interview scheduled/ongoing
        ('offer', 'Offer Extended'),             # Company made an offer
        ('accepted', 'Accepted'),                # Student accepted the offer
        ('rejected', 'Rejected'),                # Application rejected
        ('withdrawn', 'Withdrawn'),              # Student withdrew application
    ]

    # ---- Relationships ----
    # The student who submitted this application
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name='student',
    )

    # The internship being applied to
    internship = models.ForeignKey(
        Internship,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name='internship',
    )

    # ---- Application Details ----
    # Cover letter or application message
    cover_letter = models.TextField(
        'cover letter',
        blank=True,
        help_text='Why are you interested in this internship?',
    )

    # Resume file uploaded with this specific application
    resume = models.FileField(
        'resume',
        upload_to='resumes/',
        blank=True,
        null=True,
    )

    # Current status in the recruitment pipeline
    status = models.CharField(
        'status',
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
    )

    # Notes from the company/recruiter (internal)
    company_notes = models.TextField(
        'company notes',
        blank=True,
        help_text='Internal notes from the recruitment team',
    )

    # Reason for rejection (if rejected)
    rejection_reason = models.TextField(
        'rejection reason',
        blank=True,
    )

    # Academic Supervisor details
    supervisor_email = models.EmailField(
        'supervisor email',
        blank=True,
        help_text='Academic supervisor email provided during application',
    )

    assigned_supervisor = models.ForeignKey(
        'accounts.SupervisorProfile',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='assigned_applications',
        verbose_name='assigned supervisor',
    )

    # ---- AI Analysis (for future AI features) ----
    # AI-generated match score (0-100)
    ai_match_score = models.PositiveIntegerField(
        'AI match score',
        blank=True,
        null=True,
        help_text='AI-calculated compatibility score (0-100)',
    )

    # Detailed AI multi-factor breakdown (skills, experience, education, formatting, matched/missing skills, notes)
    ai_breakdown = models.JSONField(
        'AI match breakdown',
        default=dict,
        blank=True,
        help_text='Detailed analytical scoring breakdown and CV formatting review',
    )

    # ---- Timestamps ----
    applied_at = models.DateTimeField('applied at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)

    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
        ordering = ['-applied_at']
        # Prevent duplicate applications from same student to same internship
        unique_together = ['student', 'internship']

    def __str__(self):
        return f"{self.student.user.get_full_name()} → {self.internship.title}"

    @property
    def status_color(self):
        """Return Bootstrap color class for current status."""
        colors = {
            'pending': 'warning',
            'reviewing': 'info',
            'assessment': 'primary',
            'interview': 'primary',
            'offer': 'success',
            'accepted': 'success',
            'rejected': 'danger',
            'withdrawn': 'secondary',
        }
        return colors.get(self.status, 'secondary')
