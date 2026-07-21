"""
============================================================
Notifications Views - In-App Notification Center
============================================================
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from notifications.models import Notification


@login_required
def list(request):
    """List all notifications for the current user."""
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'mark_all_read':
            request.user.notifications.filter(is_read=False).update(
                is_read=True,
                read_at=timezone.now()
            )
            messages.success(request, 'All notifications marked as read.')
            return redirect('notifications:list')

        notification_id = request.POST.get('notification_id')
        if notification_id:
            notif = get_object_or_404(Notification, pk=notification_id, recipient=request.user)
            notif.is_read = True
            notif.read_at = timezone.now()
            notif.save()
            if notif.link:
                return redirect(notif.link)
            return redirect('notifications:list')

    notifications_list = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    context = {'notifications': notifications_list}
    return render(request, 'notifications/notification_list.html', context)
