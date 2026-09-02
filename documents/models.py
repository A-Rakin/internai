"""
============================================================
Documents Models - File Management
============================================================
Manages secure storage and organization of internship-related
documents including resumes, transcripts, certificates, etc.
============================================================
"""

from django.db import models
from django.conf import settings


class Document(models.Model):
    """
    Document uploaded by a user.
    
    Supports various document types and organizes them
    in a centralized repository for easy retrieval.
    """

    # ---- Document Type Choices ----
    TYPE_CHOICES = [
        ('resume', 'Resume / CV'),
        ('formal_photo', 'Formal Photo / Picture'),
        ('certificate', 'Certificate'),
        ('cover_letter', 'Cover Letter'),
        ('transcript', 'Academic Transcript'),
        ('portfolio', 'Portfolio'),
        ('offer_letter', 'Offer Letter'),
        ('agreement', 'Agreement'),
        ('evaluation', 'Evaluation Report'),
        ('report', 'Internship Report'),
        ('other', 'Other'),
    ]

    # ---- Relationships ----
    # The user who uploaded this document
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name='uploaded by',
    )

    # ---- Document Details ----
    # Document title/name
    title = models.CharField('title', max_length=255)

    # Document description
    description = models.TextField('description', blank=True)

    # The actual file
    file = models.FileField(
        'file',
        upload_to='documents/',
        help_text='Supported formats: PDF, DOC, DOCX, JPG, PNG',
    )

    # Document type classification
    doc_type = models.CharField(
        'document type',
        max_length=20,
        choices=TYPE_CHOICES,
        default='other',
    )

    # File size in bytes
    file_size = models.PositiveIntegerField(
        'file size',
        default=0,
        help_text='File size in bytes',
    )

    # ---- Timestamps ----
    uploaded_at = models.DateTimeField('uploaded at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)

    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.title} ({self.get_doc_type_display()})"

    @property
    def file_size_display(self):
        """Return human-readable file size."""
        if self.file_size < 1024:
            return f"{self.file_size} B"
        elif self.file_size < 1024 * 1024:
            return f"{self.file_size / 1024:.1f} KB"
        else:
            return f"{self.file_size / (1024 * 1024):.1f} MB"

    @property
    def file_extension(self):
        """Return the file extension."""
        return self.file.name.split('.')[-1].upper() if self.file else ''

    @property
    def type_icon(self):
        """Return Font Awesome icon based on document type."""
        icons = {
            'resume': 'fas fa-file-alt',
            'formal_photo': 'fas fa-user-circle',
            'cover_letter': 'fas fa-envelope-open-text',
            'transcript': 'fas fa-graduation-cap',
            'certificate': 'fas fa-certificate',
            'portfolio': 'fas fa-folder-open',
            'offer_letter': 'fas fa-handshake',
            'agreement': 'fas fa-file-contract',
            'evaluation': 'fas fa-clipboard-check',
            'report': 'fas fa-file-medical-alt',
            'other': 'fas fa-file',
        }
        return icons.get(self.doc_type, 'fas fa-file')


class ActivityLog(models.Model):
    """
    System activity log for tracking user actions.
    
    Records important user activities for audit purposes
    and admin monitoring.
    """

    # ---- Action Type Choices ----
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('register', 'Registration'),
        ('profile_update', 'Profile Update'),
        ('application_submit', 'Application Submitted'),
        ('interview_schedule', 'Interview Scheduled'),
        ('report_submit', 'Report Submitted'),
        ('evaluation_submit', 'Evaluation Submitted'),
        ('internship_create', 'Internship Created'),
        ('document_upload', 'Document Uploaded'),
        ('password_change', 'Password Changed'),
        ('other', 'Other'),
    ]

    # ---- Relationships ----
    # The user who performed the action
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='activity_logs',
        verbose_name='user',
    )

    # ---- Log Details ----
    action = models.CharField('action', max_length=30, choices=ACTION_CHOICES)
    description = models.TextField('description', blank=True)
    ip_address = models.GenericIPAddressField('IP address', blank=True, null=True)

    # ---- Timestamps ----
    created_at = models.DateTimeField('created at', auto_now_add=True)

    class Meta:
        verbose_name = 'Activity Log'
        verbose_name_plural = 'Activity Logs'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.get_action_display()}"
