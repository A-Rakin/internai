"""
============================================================
Messaging Views - Internal Communication System
============================================================
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from django.db.models import Q, Max, Count
from django.utils import timezone

from accounts.models import CustomUser
from messaging.models import Conversation, Message
from notifications.models import Notification


@login_required
def inbox(request):
    """Display user's conversations inbox."""
    conversations = Conversation.objects.filter(
        participants=request.user
    ).annotate(
        last_msg_time=Max('messages__created_at'),
        msg_count=Count('messages'),
    ).order_by('-last_msg_time')

    # Enrich each conversation with unread count and other participant
    enriched = []
    for conv in conversations:
        enriched.append({
            'conversation': conv,
            'other_user': conv.other_participant(request.user),
            'last_message': conv.last_message,
            'unread_count': conv.unread_count_for(request.user),
        })

    context = {'conversations': enriched}
    return render(request, 'messaging/inbox.html', context)


@login_required
def thread(request, pk):
    """View a conversation thread and send messages."""
    conversation = get_object_or_404(Conversation, pk=pk, participants=request.user)

    # Mark unread messages as read
    conversation.messages.filter(is_read=False).exclude(sender=request.user).update(
        is_read=True, read_at=timezone.now()
    )

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content,
            )
            conversation.save()  # Update updated_at

            # Notify the other participant
            other_user = conversation.other_participant(request.user)
            if other_user:
                Notification.objects.create(
                    recipient=other_user,
                    notification_type='system',
                    title='New Message',
                    message=f'{request.user.get_full_name()} sent you a message.',
                    link=f'/messages/thread/{conversation.pk}/',
                )
            return redirect('messaging:thread', pk=conversation.pk)

    all_messages = conversation.messages.select_related('sender').order_by('created_at')
    other_user = conversation.other_participant(request.user)

    context = {
        'conversation': conversation,
        'messages_list': all_messages,
        'other_user': other_user,
    }
    return render(request, 'messaging/thread.html', context)


@login_required
def compose(request):
    """Compose a new message / start a new conversation."""
    if request.user.role == CustomUser.STUDENT:
        django_messages.warning(request, 'Students cannot start new conversations. You can reply to messages sent to you by recruiters or supervisors.')
        return redirect('messaging:inbox')

    if request.method == 'POST':
        recipient_id = request.POST.get('recipient')
        subject = request.POST.get('subject', '').strip()
        content = request.POST.get('content', '').strip()

        if not recipient_id or not content:
            django_messages.error(request, 'Please select a recipient and write a message.')
            return redirect('messaging:compose')

        recipient = get_object_or_404(CustomUser, pk=recipient_id)

        if recipient == request.user:
            django_messages.error(request, 'You cannot message yourself.')
            return redirect('messaging:compose')

        # Check if conversation already exists between these two users
        existing = Conversation.objects.filter(
            participants=request.user
        ).filter(
            participants=recipient
        ).first()

        if existing:
            conversation = existing
            if subject:
                conversation.subject = subject
                conversation.save()
        else:
            conversation = Conversation.objects.create(subject=subject or 'Direct Message')
            conversation.participants.add(request.user, recipient)

        Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content,
        )
        conversation.save()

        # Notify recipient
        Notification.objects.create(
            recipient=recipient,
            notification_type='system',
            title='New Message',
            message=f'{request.user.get_full_name()} started a conversation with you.',
            link=f'/messages/thread/{conversation.pk}/',
        )

        django_messages.success(request, 'Message sent successfully!')
        return redirect('messaging:thread', pk=conversation.pk)

    recipient_id = request.GET.get('recipient')
    initial_subject = request.GET.get('subject', '')

    if recipient_id:
        existing = Conversation.objects.filter(
            participants=request.user
        ).filter(
            participants__pk=recipient_id
        ).first()
        if existing:
            return redirect('messaging:thread', pk=existing.pk)

    # Get all users except current user for the recipient dropdown
    users = CustomUser.objects.exclude(pk=request.user.pk).filter(is_active=True).order_by('first_name')

    context = {
        'users': users,
        'selected_recipient_id': recipient_id,
        'initial_subject': initial_subject,
    }
    return render(request, 'messaging/compose.html', context)
