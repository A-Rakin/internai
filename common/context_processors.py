def global_context(request):
    """
    Context processor to add global variables to all templates.
    """
    if request.user.is_authenticated:
        return {
            'unread_notifications_count': request.user.notifications.filter(is_read=False).count(),
            'user_role': request.user.role,
        }
    return {
        'unread_notifications_count': 0,
        'user_role': None,
    }
