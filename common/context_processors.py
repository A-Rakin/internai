def global_context(request):
    """
    Context processor to add global variables to all templates.
    Provides unread notifications count, unread messages count, and user role.
    """
    if request.user.is_authenticated:
        unread_messages = 0
        try:
            from messaging.models import Conversation
            for conv in Conversation.objects.filter(participants=request.user):
                unread_messages += conv.messages.filter(is_read=False).exclude(sender=request.user).count()
        except Exception:
            pass

        return {
            'unread_notifications_count': request.user.notifications.filter(is_read=False).count(),
            'unread_messages_count': unread_messages,
            'user_role': request.user.role,
        }
    return {
        'unread_notifications_count': 0,
        'unread_messages_count': 0,
        'user_role': None,
    }
