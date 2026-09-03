"""
============================================================
Billing Views - Package Subscriptions & Demo Payment Gateway
============================================================
Handles plan upgrades for Companies and Students, realistic
Bangladeshi mobile banking (bKash, Nagad, Upay) and Card demo
payments, instant package activations with expiration dates,
and 7-day renewal reminder notification checks.
============================================================
"""

import uuid
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from billing.models import Subscription, PaymentTransaction
from notifications.models import Notification
from documents.models import ActivityLog
from accounts.models import CompanyProfile, StudentProfile

# Plan Catalog with BDT and USD pricing
PLANS = {
    # Company Plans
    'company_basic': {
        'code': 'company_basic',
        'title': 'Basic Free',
        'category': 'company',
        'price_bdt_monthly': 0,
        'price_bdt_annual': 0,
        'price_usd_monthly': 0,
        'description': 'Essential recruitment tools for startups and small teams.',
        'features': [
            'Up to 5 Active Internship Listings',
            'Standard Applicant Review Portal',
            'PDF Resume Downloads',
            'Basic Email Notifications',
        ],
    },
    'company_pro': {
        'code': 'company_pro',
        'title': 'Pro Recruiter',
        'category': 'company',
        'price_bdt_monthly': 2000,
        'price_bdt_annual': 19200,
        'price_usd_monthly': 20,
        'description': 'Advanced AI talent matching and high-volume recruitment pipeline.',
        'features': [
            'Up to 50 Active Internship Postings',
            'AI Candidate Ranking Engine (Role-Specific)',
            'Multi-Factor AI CV Breakdown & Formatting Review',
            'Interview Scheduling & Rescheduling with Collision Guard',
            'Direct Messaging with Candidates and Supervisors',
            'Recruiter Evaluation Notes & Scorecards',
        ],
    },
    'company_ultimate': {
        'code': 'company_ultimate',
        'title': 'Ultimate Enterprise',
        'category': 'company',
        'price_bdt_monthly': 8000,
        'price_bdt_annual': 76800,
        'price_usd_monthly': 80,
        'description': 'Complete enterprise talent acquisition suite with dedicated support.',
        'features': [
            'Unlimited Active Internship Postings',
            'Everything in Pro Recruiter',
            'Dedicated Enterprise Account Manager',
            'Custom University Branding & Partnerships',
            'Automated Supervisor Assignment & Sync',
            'Full Platform Activity & Recruitment Audit Logs',
            '24/7 Priority Phone & Email Support',
        ],
    },

    # Student Career Plans
    'student_basic': {
        'code': 'student_basic',
        'title': 'Student Basic Free',
        'category': 'student',
        'price_bdt_monthly': 0,
        'price_bdt_annual': 0,
        'price_usd_monthly': 0,
        'description': 'Free starter pack for exploring early career internships.',
        'features': [
            'Apply to up to 10 Internships / month',
            'Standard Student Profile Builder',
            'PDF Resume & Certificate Vault',
            'Real-Time Application Status Alerts',
            'View Recruiter Feedback Notes & Advice',
        ],
    },
    'student_pro': {
        'code': 'student_pro',
        'title': 'Student Pro',
        'category': 'student',
        'price_bdt_monthly': 199,
        'price_bdt_annual': 1990,
        'price_usd_monthly': 2,
        'description': 'Affordable monthly boost for active job seekers.',
        'features': [
            'Apply to up to 50 Internships / month',
            'Instant AI Resume Match Score & Skill Gap Insights',
            '10 AI Tailored Cover Letters / month',
            'Priority Application Flagging in Recruiter Dashboard',
            'Weekly Academic Report Submissions & Evaluations',
            'Multi-Document Storage Vault',
        ],
    },
    'student_boost': {
        'code': 'student_boost',
        'title': 'Student Career Boost',
        'category': 'student',
        'price_bdt_monthly': 499,
        'price_bdt_annual': 4990,
        'price_usd_monthly': 5,
        'description': 'The ultimate preparation suite for dream corporate placements.',
        'features': [
            'Unlimited Internship Applications / month',
            'Everything in Student Pro',
            'Unlimited AI Cover Letters',
            'AI Mock Interview Coach with Instant Scoring & Feedback',
            'Top Candidate Gold Badge on Applications',
            'Automated University Supervisor Linking & Verification',
            'Priority 1-on-1 Career Support',
        ],
    },
}

# Aliases for backwards compatibility with legacy urls
PLAN_ALIASES = {
    'pro': 'company_pro',
    'ultimate': 'company_ultimate',
    'basic': 'company_basic',
}


def get_plan_info(plan_code):
    """Normalize plan code and return plan configuration dictionary."""
    normalized = PLAN_ALIASES.get(plan_code.lower(), plan_code.lower())
    return PLANS.get(normalized)


@login_required
def checkout(request, plan_code):
    """
    Render realistic demo checkout page with Bangladeshi Mobile Banking
    (bKash, Nagad, Upay) and Credit/Debit Card options.
    """
    plan = get_plan_info(plan_code)
    if not plan:
        messages.error(request, f"Invalid subscription plan '{plan_code}' selected.")
        return redirect('landing:pricing')

    billing_cycle = request.GET.get('cycle', 'monthly').lower()
    if billing_cycle not in ['monthly', 'annual']:
        billing_cycle = 'monthly'

    # Determine amount in BDT
    if billing_cycle == 'annual':
        amount = plan['price_bdt_annual']
    else:
        amount = plan['price_bdt_monthly']

    # Free plan instant activation
    if amount == 0:
        return _activate_free_plan(request, plan)

    context = {
        'plan': plan,
        'billing_cycle': billing_cycle,
        'amount': amount,
        'currency': 'BDT',
    }
    return render(request, 'billing/checkout.html', context)


@login_required
def process_demo_payment(request):
    """
    Simulate payment processing for bKash, Nagad, Upay, or Card.
    Creates subscription record with 30-day or 365-day validity,
    generates transaction receipt, and activates user tier.
    """
    if request.method != 'POST':
        return redirect('landing:pricing')

    plan_code = request.POST.get('plan_code', '')
    billing_cycle = request.POST.get('billing_cycle', 'monthly')
    payment_method = request.POST.get('payment_method', 'bkash')
    account_number = request.POST.get('account_number', '').strip()
    card_number = request.POST.get('card_number', '').strip()

    plan = get_plan_info(plan_code)
    if not plan:
        messages.error(request, 'Invalid plan selected.')
        return redirect('landing:pricing')

    amount = plan['price_bdt_annual'] if billing_cycle == 'annual' else plan['price_bdt_monthly']
    duration_days = 365 if billing_cycle == 'annual' else 30

    # Mask account or card number for privacy
    if payment_method in ['bkash', 'nagad', 'upay']:
        if len(account_number) >= 8:
            masked_number = account_number[:3] + '****' + account_number[-4:]
        else:
            masked_number = '017****' + str(uuid.uuid4().int)[:4]
    else:
        # Card
        clean_card = card_number.replace(' ', '').replace('-', '')
        if len(clean_card) >= 12:
            masked_number = '**** **** **** ' + clean_card[-4:]
        else:
            masked_number = '**** **** **** 4242'

    # Generate realistic unique transaction ID
    prefix = payment_method.upper()
    random_digits = str(uuid.uuid4().int)[:8]
    transaction_id = f"TXN-{prefix}-{random_digits}"

    # Calculate validity window
    now = timezone.now()
    expires_at = now + timedelta(days=duration_days)

    # Deactivate any existing active subscriptions for this user
    Subscription.objects.filter(user=request.user, is_active=True).update(is_active=False)

    # Create new active Subscription
    subscription = Subscription.objects.create(
        user=request.user,
        plan_name=plan['code'],
        plan_display_name=plan['title'],
        plan_category=plan['category'],
        billing_cycle=billing_cycle,
        amount=Decimal(str(amount)),
        currency='BDT',
        started_at=now,
        expires_at=expires_at,
        is_active=True,
        warning_notified=False,
    )

    # If company, update legacy field for compatibility
    if hasattr(request.user, 'company_profile'):
        company = request.user.company_profile
        if 'ultimate' in plan['code']:
            company.subscription_plan = 'ultimate'
        elif 'pro' in plan['code']:
            company.subscription_plan = 'pro'
        else:
            company.subscription_plan = 'basic'
        company.save()

    # Record Payment Transaction
    txn = PaymentTransaction.objects.create(
        user=request.user,
        subscription=subscription,
        transaction_id=transaction_id,
        payment_method=payment_method,
        account_number=masked_number,
        amount=Decimal(str(amount)),
        currency='BDT',
        status='completed',
    )

    # Send in-app notification to user
    Notification.objects.create(
        recipient=request.user,
        notification_type='system',
        title=f'🎉 Package Activated: {plan["title"]}',
        message=(
            f'Payment of ৳{amount:,.2f} BDT via {txn.get_payment_method_display()} was verified. '
            f'Your {plan["title"]} is active until {expires_at.strftime("%B %d, %Y")} '
            f'(Txn ID: {transaction_id}).'
        ),
        link=reverse('billing:receipt', kwargs={'transaction_id': transaction_id}),
        priority='high',
    )

    # Log activity
    ActivityLog.objects.create(
        user=request.user,
        action='other',
        description=f'Subscribed to {plan["title"]} ({billing_cycle}) via {txn.get_payment_method_display()}',
    )

    messages.success(
        request,
        f"🎉 Congratulations! Your '{plan['title']}' package is now active for {duration_days} days."
    )
    return redirect('billing:receipt', transaction_id=transaction_id)


def _activate_free_plan(request, plan):
    """Handle instant activation of free basic tiers."""
    now = timezone.now()
    expires_at = now + timedelta(days=365) # Free tier lasts 1 year before renew

    Subscription.objects.filter(user=request.user, is_active=True).update(is_active=False)

    subscription = Subscription.objects.create(
        user=request.user,
        plan_name=plan['code'],
        plan_display_name=plan['title'],
        plan_category=plan['category'],
        billing_cycle='annual',
        amount=Decimal('0.00'),
        currency='BDT',
        started_at=now,
        expires_at=expires_at,
        is_active=True,
    )

    if hasattr(request.user, 'company_profile'):
        company = request.user.company_profile
        company.subscription_plan = 'basic'
        company.save()
        return redirect('companies:dashboard')
    elif hasattr(request.user, 'student_profile'):
        return redirect('students:dashboard')

    return redirect('landing:pricing')


@login_required
def receipt(request, transaction_id):
    """Display printable transaction receipt and package activation invoice."""
    txn = get_object_or_404(PaymentTransaction, transaction_id=transaction_id, user=request.user)
    subscription = txn.subscription

    context = {
        'txn': txn,
        'subscription': subscription,
    }
    return render(request, 'billing/receipt.html', context)


@login_required
def my_package(request):
    """Display the active package overview for the logged-in company or student."""
    subscription = Subscription.objects.filter(user=request.user, is_active=True).order_by('-started_at').first()
    past_subscriptions = Subscription.objects.filter(user=request.user).exclude(pk=subscription.pk if subscription else None)
    transactions = PaymentTransaction.objects.filter(user=request.user).order_by('-created_at')[:5]

    context = {
        'subscription': subscription,
        'past_subscriptions': past_subscriptions,
        'transactions': transactions,
    }
    return render(request, 'billing/my_package.html', context)


def check_and_notify_expiring_packages(user):
    """
    Utility helper: checks if the user's active subscription is within 7 days of expiry.
    If so and not already alerted for this cycle, fires a reminder notification.
    """
    subscription = Subscription.objects.filter(user=user, is_active=True).order_by('-started_at').first()
    if not subscription:
        return

    if subscription.is_expired:
        subscription.is_active = False
        subscription.save(update_fields=['is_active'])

        Notification.objects.get_or_create(
            recipient=user,
            notification_type='system',
            title='⚠️ Package Expired',
            defaults={
                'message': (
                    f'Your {subscription.plan_display_name} subscription has expired. '
                    'Please renew your package to restore premium recruitment or application features.'
                ),
                'link': reverse('landing:pricing'),
                'priority': 'high',
            }
        )
    elif subscription.is_expiring_soon and not subscription.warning_notified:
        days = subscription.days_remaining
        Notification.objects.create(
            recipient=user,
            notification_type='system',
            title='⏳ Package Expiration Reminder',
            message=(
                f'Your {subscription.plan_display_name} package will expire in {days} day{"s" if days != 1 else ""} '
                f'(on {subscription.expires_at.strftime("%B %d, %Y")}). '
                'Please renew your package to avoid service interruptions.'
            ),
            link=reverse('landing:pricing'),
            priority='high',
        )
        subscription.warning_notified = True
        subscription.save(update_fields=['warning_notified'])


# Legacy endpoints maintained for backwards compatibility
@login_required
def create_checkout_session(request, plan_name):
    """Legacy route redirecting to new interactive checkout."""
    return checkout(request, plan_name)


@login_required
def payment_success(request):
    """Legacy callback redirecting to pricing."""
    return redirect('billing:my_package')


def payment_cancel(request):
    """Legacy callback redirecting to pricing."""
    messages.info(request, 'Checkout was cancelled.')
    return redirect('landing:pricing')
