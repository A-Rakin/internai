"""
============================================================
Messaging Models - Internal Communication System
============================================================
Direct messaging between platform users (students, companies,
supervisors) with conversation threading and read tracking.
============================================================
"""

from django.db import models
from django.conf import settings


class Conversation(models.Model):
    """
    A conversation thread between two users.
    Stores metadata about the conversation and participants.
    """
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations',
        verbose_name='participants',
    )

    subject = models.CharField(
        'subject',
        max_length=255,
        blank=True,
        default='',
    )

    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)

    class Meta:
        verbose_name = 'Conversation'
        verbose_name_plural = 'Conversations'
        ordering = ['-updated_at']

    def __str__(self):
        return self.subject or f"Conversation #{self.pk}"

    @property
    def last_message(self):
        """Return the most recent message in this conversation."""
        return self.messages.order_by('-created_at').first()

    def unread_count_for(self, user):
        """Return count of unread messages for a specific user."""
        return self.messages.filter(is_read=False).exclude(sender=user).count()

    def other_participant(self, user):
        """Return the other participant in the conversation."""
        return self.participants.exclude(pk=user.pk).first()


class Message(models.Model):
    """
    A single message within a conversation thread.
    """
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='conversation',
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name='sender',
    )

    content = models.TextField('message content')

    is_read = models.BooleanField('read', default=False)
    read_at = models.DateTimeField('read at', blank=True, null=True)

    created_at = models.DateTimeField('created at', auto_now_add=True)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.get_full_name()}: {self.content[:50]}"
