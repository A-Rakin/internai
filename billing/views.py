"""
============================================================
Billing Views - Stripe Payment Gateway Integration
============================================================
Handles Stripe Checkout Sessions for Pro ($20) and Ultimate ($80)
subscription plan upgrades, success/cancel redirects, and plan activation.
============================================================
"""

import stripe
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.urls import reverse

from accounts.models import CompanyProfile
from notifications.models import Notification
from documents.models import ActivityLog

stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')


@login_required
def create_checkout_session(request, plan_name):
    """
    Create a Stripe Checkout Session for subscription upgrade.
    Supports 'pro' ($20/mo) and 'ultimate' ($80/mo).
    """
    plan_name = plan_name.lower()
    if plan_name not in ['pro', 'ultimate']:
        messages.error(request, 'Invalid subscription plan selected.')
        return redirect('landing:pricing')

    # Ensure user has a company profile (or auto-convert/notify)
    if not hasattr(request.user, 'company_profile'):
        messages.info(request, 'Please register or switch to a Company account to upgrade recruitment plans.')
        return redirect('accounts:register_company')

    company = request.user.company_profile

    # Define prices in cents (USD)
    prices = {
        'pro': 2000,      # $20.00 USD
        'ultimate': 8000, # $80.00 USD
    }
    amount = prices[plan_name]

    # Domain for redirects
    domain_url = request.build_absolute_uri('/')[:-1]

    try:
        if stripe.api_key and not stripe.api_key.startswith('sk_test_51Pxxxxxxxxx'):
            # Real Stripe Checkout Session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f'InternAI {plan_name.title()} Subscription Plan',
                            'description': f'Access to InternAI {plan_name.title()} features.',
                        },
                        'unit_amount': amount,
                        'recurring': {'interval': 'month'},
                    },
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=domain_url + reverse('billing:success') + f'?plan={plan_name}&session_id={{CHECKOUT_SESSION_ID}}',
                cancel_url=domain_url + reverse('billing:cancel'),
                client_reference_id=str(request.user.pk),
            )
            return redirect(checkout_session.url, code=303)
        else:
            # Fallback Development Mode: Simulate instant upgrade
            company.subscription_plan = plan_name
            company.save()

            Notification.objects.create(
                recipient=request.user,
                notification_type='system',
                title=f'Subscribed to {plan_name.title()} Plan!',
                message=f'Your company subscription has been upgraded to {plan_name.title()} ($ {amount//100}/mo).',
                link='/company/profile/',
                priority='high',
            )

            ActivityLog.objects.create(
                user=request.user,
                action='other',
                description=f'Upgraded subscription to {plan_name.title()} plan ($ {amount//100}/mo)',
            )

            messages.success(request, f'🎉 Success! Your company subscription is now active on the {plan_name.title()} Plan ($ {amount//100}/mo).')
            return redirect('companies:dashboard')

    except Exception as e:
        messages.error(request, f'Stripe Error: {str(e)}')
        return redirect('landing:pricing')


@login_required
def payment_success(request):
    """Callback page after successful Stripe payment."""
    plan_name = request.GET.get('plan', 'pro')

    if hasattr(request.user, 'company_profile'):
        company = request.user.company_profile
        company.subscription_plan = plan_name
        company.save()

        Notification.objects.create(
            recipient=request.user,
            notification_type='system',
            title=f'Plan Upgraded to {plan_name.title()}',
            message=f'Payment confirmed! Your active plan is now {plan_name.title()}.',
            link='/company/profile/',
            priority='high',
        )

        messages.success(request, f'🎉 Payment successful! Your account has been upgraded to the {plan_name.title()} Plan.')
        return redirect('companies:dashboard')

    messages.success(request, 'Payment processed successfully!')
    return redirect('landing:home')


def payment_cancel(request):
    """Callback page when user cancels Stripe checkout."""
    messages.info(request, 'Payment process was cancelled. You have not been charged.')
    return redirect('landing:pricing')
