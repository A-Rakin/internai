"""
============================================================
Notifications Email Service
============================================================
Handles HTML and plain text email generation and SMTP delivery
for platform notifications and events (interviews, supervisor
assignments, application updates, system alerts, etc.).
============================================================
"""

import logging
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

logger = logging.getLogger(__name__)


def get_type_badge_color(notification_type):
    """Return badge color code for email header based on type."""
    colors = {
        'application': '#4F46E5',  # Indigo
        'interview': '#0EA5E9',    # Sky Blue
        'report': '#F59E0B',       # Amber
        'evaluation': '#10B981',   # Emerald
        'internship': '#6366F1',   # Indigo
        'system': '#64748B',       # Slate
        'reminder': '#EC4899',     # Pink
        'offer': '#059669',        # Green
    }
    return colors.get(notification_type, '#4F46E5')


def send_notification_email(notification):
    """
    Send formatted HTML and Plain Text email for a given Notification model instance.
    
    Wrapped in try-except to ensure database actions and application requests
    are never interrupted even if SMTP credentials are unavailable or network fails.
    """
    recipient_email = getattr(notification.recipient, 'email', None)
    if not recipient_email:
        logger.warning(f"Notification {notification.id} skipped email: Recipient has no email address.")
        return False

    recipient_name = notification.recipient.get_full_name() or notification.recipient.username or "User"
    subject = f"[InternAI] {notification.title}"
    badge_color = get_type_badge_color(notification.notification_type)
    type_display = notification.get_notification_type_display().upper()
    
    # Resolve absolute link if relative link provided
    site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
    action_link = notification.link
    if action_link and action_link.startswith('/'):
        action_link = f"{site_url.rstrip('/')}{action_link}"

    # HTML Email Body
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{notification.title}</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Helvetica, Arial, sans-serif; background-color: #f1f5f9; color: #1e293b;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed; background-color: #f1f5f9; padding: 30px 10px;">
            <tr>
                <td align="center">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.08);">
                        
                        <!-- Header -->
                        <tr>
                            <td style="background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%); padding: 28px 32px; text-align: left;">
                                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                    <tr>
                                        <td>
                                            <span style="font-size: 24px; font-weight: 800; color: #ffffff; letter-spacing: -0.5px;">
                                                Intern<span style="color: #818cf8;">AI</span>
                                            </span>
                                        </td>
                                        <td align="right">
                                            <span style="display: inline-block; background-color: {badge_color}; color: #ffffff; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 20px; letter-spacing: 0.5px;">
                                                {type_display}
                                            </span>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>

                        <!-- Body Content -->
                        <tr>
                            <td style="padding: 32px 32px 24px 32px;">
                                <h2 style="margin: 0 0 12px 0; color: #0f172a; font-size: 20px; font-weight: 700; line-height: 1.3;">
                                    {notification.title}
                                </h2>
                                <p style="margin: 0 0 20px 0; font-size: 14px; color: #64748b; line-height: 1.5;">
                                    Hello <strong>{recipient_name}</strong>,
                                </p>
                                
                                <div style="background-color: #f8fafc; border-left: 4px solid {badge_color}; padding: 18px; border-radius: 0 8px 8px 0; margin-bottom: 24px;">
                                    <p style="margin: 0; font-size: 15px; color: #334155; line-height: 1.6; white-space: pre-line;">
                                        {notification.message}
                                    </p>
                                </div>

                                {"" if not action_link else f'''
                                <div style="text-align: center; margin: 28px 0;">
                                    <a href="{action_link}" target="_blank" style="display: inline-block; background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%); color: #ffffff; font-size: 14px; font-weight: 600; text-decoration: none; padding: 12px 28px; border-radius: 8px; box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);">
                                        View Details on InternAI &rarr;
                                    </a>
                                </div>
                                '''}
                            </td>
                        </tr>

                        <!-- Footer -->
                        <tr>
                            <td style="background-color: #f8fafc; border-top: 1px solid #e2e8f0; padding: 20px 32px; text-align: center;">
                                <p style="margin: 0 0 6px 0; font-size: 12px; color: #94a3b8;">
                                    This is an automated notification from <strong>InternAI Platform</strong>.
                                </p>
                                <p style="margin: 0; font-size: 11px; color: #cbd5e1;">
                                    &copy; 2026 InternAI. All rights reserved.
                                </p>
                            </td>
                        </tr>

                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

    # Plain Text Fallback
    text_content = f"""
InternAI Notification: {notification.title}

Hello {recipient_name},

{notification.message}

{f"View details: {action_link}" if action_link else ""}

---
InternAI Platform Automated Email
    """

    try:
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'InternAI <noreply@internai.com>')
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content.strip(),
            from_email=from_email,
            to=[recipient_email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)
        logger.info(f"Notification email sent successfully to {recipient_email} for Notification ID {notification.id}")
        return True
    except Exception as e:
        # Catch network error, missing credentials, or invalid SMTP settings gracefully
        logger.warning(f"Could not send email to {recipient_email} (Notification ID {notification.id}): {e}")
        return False
