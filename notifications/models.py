"""
============================================================
Notifications Models - In-App Notifications
============================================================
Manages notification delivery for all user roles,
including application updates, interview reminders,
report deadlines, and system alerts.
============================================================
"""

from django.db import models
from django.conf import settings


class Notification(models.Model):
    """
    In-app notification for platform events.
    
    Automatically generated when significant events occur
    such as application submissions, interview scheduling,
    report deadlines, and supervisor feedback.
    """

    # ---- Notification Type Choices ----
    TYPE_CHOICES = [
        ('application', 'Application Update'),
        ('interview', 'Interview'),
        ('report', 'Report'),
        ('evaluation', 'Evaluation'),
        ('internship', 'Internship'),
        ('system', 'System'),
        ('reminder', 'Reminder'),
        ('offer', 'Offer'),
    ]

    # ---- Priority Choices ----
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    # ---- Relationships ----
    # The user receiving this notification
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='recipient',
    )

    # ---- Notification Content ----
    # Notification type for categorization and icon display
    notification_type = models.CharField(
        'type',
        max_length=20,
        choices=TYPE_CHOICES,
        default='system',
    )

    # Notification title
    title = models.CharField('title', max_length=255)

    # Notification message body
    message = models.TextField('message')

    # Priority level
    priority = models.CharField(
        'priority',
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
    )

    # Link to related page (optional)
    link = models.CharField(
        'link',
        max_length=500,
        blank=True,
        help_text='URL to the related page',
    )

    # ---- Status ----
    # Whether the notification has been read
    is_read = models.BooleanField('read', default=False)

    # ---- Timestamps ----
    created_at = models.DateTimeField('created at', auto_now_add=True)
    read_at = models.DateTimeField('read at', blank=True, null=True)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} → {self.recipient.email}"

    @property
    def type_icon(self):
        """Return Font Awesome icon class based on notification type."""
        icons = {
            'application': 'fas fa-file-alt',
            'interview': 'fas fa-calendar-check',
            'report': 'fas fa-clipboard-list',
            'evaluation': 'fas fa-star',
            'internship': 'fas fa-briefcase',
            'system': 'fas fa-bell',
            'reminder': 'fas fa-clock',
            'offer': 'fas fa-handshake',
        }
        return icons.get(self.notification_type, 'fas fa-bell')

    @property
    def type_color(self):
        """Return Bootstrap color class based on notification type."""
        colors = {
            'application': 'primary',
            'interview': 'info',
            'report': 'warning',
            'evaluation': 'success',
            'internship': 'primary',
            'system': 'secondary',
            'reminder': 'warning',
            'offer': 'success',
        }
        return colors.get(self.notification_type, 'secondary')
