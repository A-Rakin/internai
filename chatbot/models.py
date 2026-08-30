"""
============================================================
Chatbot Models - AI-Powered Assistant
============================================================
Stores chat sessions and messages for the AI chatbot
powered by Groq Cloud AI (Llama 3.3).
============================================================
"""

from django.db import models
from django.conf import settings


class ChatSession(models.Model):
    """A chat session between a user and the AI assistant."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chat_sessions',
        verbose_name='user',
    )

    title = models.CharField('session title', max_length=255, default='New Chat')
    is_active = models.BooleanField('active', default=True)

    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)

    class Meta:
        verbose_name = 'Chat Session'
        verbose_name_plural = 'Chat Sessions'
        ordering = ['-updated_at']

    def __str__(self):
        return f"Chat: {self.user.get_full_name()} - {self.title}"


class ChatMessage(models.Model):
    """A single message in a chat session (user or AI)."""
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'AI Assistant'),
    ]

    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='session',
    )

    role = models.CharField('role', max_length=10, choices=ROLE_CHOICES)
    content = models.TextField('content')

    created_at = models.DateTimeField('created at', auto_now_add=True)

    class Meta:
        verbose_name = 'Chat Message'
        verbose_name_plural = 'Chat Messages'
        ordering = ['created_at']

    def __str__(self):
        return f"[{self.role}] {self.content[:50]}"
