"""
============================================================
Reports Models - Weekly Reports & Evaluations
============================================================
Manages student weekly internship reports and supervisor
evaluations throughout the internship period.
============================================================
"""

from django.db import models
from accounts.models import StudentProfile, SupervisorProfile
from internships.models import Internship


class WeeklyReport(models.Model):
    """
    Weekly internship report submitted by a student.
    
    Students submit weekly reports detailing their activities,
    challenges, and plans. Supervisors review and score these.
    """

    # ---- Status Choices ----
    STATUS_CHOICES = [
        ('draft', 'Draft'),            # Not yet submitted
        ('submitted', 'Submitted'),    # Submitted for review
        ('reviewed', 'Reviewed'),      # Reviewed by supervisor
        ('approved', 'Approved'),      # Approved by supervisor
        ('rejected', 'Rejected'),      # Rejected - needs revision
    ]

    # ---- Relationships ----
    # The student submitting the report
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='weekly_reports',
        verbose_name='student',
    )

    # The internship this report is for
    internship = models.ForeignKey(
        Internship,
        on_delete=models.CASCADE,
        related_name='weekly_reports',
        verbose_name='internship',
    )

    # The supervisor reviewing this report (optional - assigned later)
    supervisor = models.ForeignKey(
        SupervisorProfile,
        on_delete=models.SET_NULL,
        related_name='reviewed_reports',
        verbose_name='supervisor',
        blank=True,
        null=True,
    )

    # ---- Report Details ----
    # Week number (1, 2, 3, etc.)
    week_number = models.PositiveIntegerField(
        'week number',
        help_text='Week number of the internship (e.g., 1, 2, 3)',
    )

    # Report title
    title = models.CharField(
        'report title',
        max_length=255,
        help_text='Brief title summarizing this week\'s work',
    )

    # What was accomplished this week
    activities = models.TextField(
        'activities completed',
        help_text='Describe what you accomplished this week',
    )

    # Challenges faced
    challenges = models.TextField(
        'challenges faced',
        blank=True,
        help_text='Describe any challenges or difficulties encountered',
    )

    # Plan for next week
    next_week_plan = models.TextField(
        'next week plan',
        blank=True,
        help_text='What do you plan to work on next week?',
    )

    # Hours worked this week
    hours_worked = models.DecimalField(
        'hours worked',
        max_digits=5,
        decimal_places=1,
        default=40,
    )

    # ---- Status & Review ----
    # Current status of the report
    status = models.CharField(
        'status',
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
    )

    # Supervisor feedback
    feedback = models.TextField(
        'supervisor feedback',
        blank=True,
    )

    # Score given by supervisor (0-100)
    score = models.PositiveIntegerField(
        'score',
        blank=True,
        null=True,
        help_text='Score out of 100',
    )

    # ---- Timestamps ----
    submitted_at = models.DateTimeField('submitted at', blank=True, null=True)
    reviewed_at = models.DateTimeField('reviewed at', blank=True, null=True)
    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)

    class Meta:
        verbose_name = 'Weekly Report'
        verbose_name_plural = 'Weekly Reports'
        ordering = ['-week_number']
        # One report per student per week per internship
        unique_together = ['student', 'internship', 'week_number']

    def __str__(self):
        return f"Week {self.week_number} - {self.student.user.get_full_name()}"


class Evaluation(models.Model):
    """
    Supervisor evaluation of a student's internship performance.
    
    Provides multi-criteria scoring for technical skills,
    communication, professionalism, attendance, and overall performance.
    """

    # ---- Relationships ----
    # The supervisor performing the evaluation
    supervisor = models.ForeignKey(
        SupervisorProfile,
        on_delete=models.CASCADE,
        related_name='evaluations',
        verbose_name='supervisor',
    )

    # The student being evaluated
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='evaluations',
        verbose_name='student',
    )

    # The internship being evaluated
    internship = models.ForeignKey(
        Internship,
        on_delete=models.CASCADE,
        related_name='evaluations',
        verbose_name='internship',
    )

    # ---- Evaluation Scores (1-10 scale) ----
    # Technical competency
    technical_score = models.PositiveIntegerField(
        'technical competency',
        help_text='Score from 1 to 10',
    )

    # Communication skills
    communication_score = models.PositiveIntegerField(
        'communication skills',
        help_text='Score from 1 to 10',
    )

    # Professionalism
    professionalism_score = models.PositiveIntegerField(
        'professionalism',
        help_text='Score from 1 to 10',
    )

    # Attendance and punctuality
    attendance_score = models.PositiveIntegerField(
        'attendance',
        help_text='Score from 1 to 10',
    )

    # Overall performance
    overall_score = models.PositiveIntegerField(
        'overall performance',
        help_text='Score from 1 to 10',
    )

    # ---- Feedback ----
    # Detailed evaluation comments
    comments = models.TextField(
        'evaluation comments',
        help_text='Detailed feedback on the student\'s performance',
    )

    # Recommendation
    recommendation = models.TextField(
        'recommendation',
        blank=True,
        help_text='Any recommendations for the student',
    )

    # Whether this is the final evaluation
    is_final = models.BooleanField(
        'final evaluation',
        default=False,
    )

    # ---- Timestamps ----
    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)

    class Meta:
        verbose_name = 'Evaluation'
        verbose_name_plural = 'Evaluations'
        ordering = ['-created_at']

    def __str__(self):
        return f"Evaluation: {self.student.user.get_full_name()} by {self.supervisor.user.get_full_name()}"

    @property
    def average_score(self):
        """Calculate the average of all evaluation criteria."""
        scores = [
            self.technical_score,
            self.communication_score,
            self.professionalism_score,
            self.attendance_score,
            self.overall_score,
        ]
        return sum(scores) / len(scores)
