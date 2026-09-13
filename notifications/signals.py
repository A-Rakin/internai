"""
============================================================
Notifications Signal Handlers
============================================================
Listens for Notification post_save signals to automatically
dispatch emails for all platform notifications.
============================================================
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from .emails import send_notification_email


@receiver(post_save, sender=Notification)
def notification_post_save_email_handler(sender, instance, created, **kwargs):
    """
    Trigger automated email delivery whenever a new Notification is created.
    """
    if created:
        send_notification_email(instance)
