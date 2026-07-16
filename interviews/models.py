"""
============================================================
Interviews Models - Interview Scheduling
============================================================
Manages interview scheduling, meeting links, outcomes,
and notes for the recruitment process.
============================================================
"""

from django.db import models
from applications.models import Application


class Interview(models.Model):
    """
    Interview record for a specific application.
    
    Tracks interview scheduling, type, meeting details,
    and outcomes throughout the interview process.
    """

    # ---- Interview Type Choices ----
    TYPE_CHOICES = [
        ('technical', 'Technical Interview'),
        ('hr', 'HR Interview'),
        ('behavioral', 'Behavioral Interview'),
        ('group', 'Group Interview'),
        ('final', 'Final Interview'),
    ]

    # ---- Mode Choices ----
    MODE_CHOICES = [
        ('online', 'Online'),          # Video call
        ('onsite', 'On-site'),         # In-person
        ('phone', 'Phone Call'),       # Phone interview
    ]

    # ---- Outcome Choices ----
    OUTCOME_CHOICES = [
        ('pending', 'Pending'),        # Not yet conducted
        ('passed', 'Passed'),          # Candidate passed
        ('failed', 'Failed'),          # Candidate failed
        ('no_show', 'No Show'),        # Candidate didn't attend
        ('rescheduled', 'Rescheduled'), # Interview was rescheduled
    ]

    # ---- Relationships ----
    # The application this interview is for
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='interviews',
        verbose_name='application',
    )

    # ---- Interview Details ----
    # Type of interview
    interview_type = models.CharField(
        'interview type',
        max_length=20,
        choices=TYPE_CHOICES,
        default='technical',
    )

    # Interview mode (online/onsite/phone)
    mode = models.CharField(
        'interview mode',
        max_length=20,
        choices=MODE_CHOICES,
        default='online',
    )

    # Scheduled date and time
    scheduled_at = models.DateTimeField(
        'scheduled date & time',
    )

    # Duration in minutes
    duration_minutes = models.PositiveIntegerField(
        'duration (minutes)',
        default=60,
    )

    # Meeting link for online interviews
    meeting_link = models.URLField(
        'meeting link',
        blank=True,
        help_text='Video call link (Google Meet, Zoom, etc.)',
    )

    # Location for onsite interviews
    location = models.CharField(
        'location',
        max_length=255,
        blank=True,
        help_text='Address for on-site interviews',
    )

    # Interviewer name
    interviewer_name = models.CharField(
        'interviewer name',
        max_length=255,
        blank=True,
    )

    # ---- Outcome ----
    # Interview result
    outcome = models.CharField(
        'outcome',
        max_length=20,
        choices=OUTCOME_CHOICES,
        default='pending',
    )

    # Interview notes/feedback
    notes = models.TextField(
        'interview notes',
        blank=True,
        help_text='Notes and feedback from the interview',
    )

    # Score given by interviewer (optional)
    score = models.PositiveIntegerField(
        'interview score',
        blank=True,
        null=True,
        help_text='Score out of 100',
    )

    # ---- Timestamps ----
    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)

    class Meta:
        verbose_name = 'Interview'
        verbose_name_plural = 'Interviews'
        ordering = ['scheduled_at']

    def __str__(self):
        return f"{self.get_interview_type_display()} - {self.application}"
