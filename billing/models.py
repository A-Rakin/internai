"""
============================================================
Billing Models - Subscriptions & Payment Transactions
============================================================
Handles subscription plans for companies and students,
expiration tracking, 7-day expiry warning states, and
Bangladeshi mobile banking / card transaction logs.
============================================================
"""

from django.db import models
from django.utils import timezone
from datetime import timedelta
from accounts.models import CustomUser


class Subscription(models.Model):
    """
    Tracks active/past subscription plans for companies and students.
    Includes expiration dates, 7-day renewal notification status, and pricing.
    """

    PLAN_CATEGORIES = [
        ('company', 'Company Recruitment Plan'),
        ('student', 'Student Career Plan'),
    ]

    BILLING_CYCLES = [
        ('monthly', 'Monthly Billing'),
        ('annual', 'Annual Billing'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expiring', 'Expiring Soon (Within 7 Days)'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='subscriber',
    )

    plan_name = models.CharField(
        'plan identifier',
        max_length=50,
        help_text='Internal code: pro, ultimate, student_pro, student_boost, basic',
    )

    plan_display_name = models.CharField(
        'plan display title',
        max_length=100,
        help_text='User facing title: Pro Recruiter, Student Career Boost, etc.',
    )

    plan_category = models.CharField(
        'plan category',
        max_length=20,
        choices=PLAN_CATEGORIES,
        default='company',
    )

    billing_cycle = models.CharField(
        'billing cycle',
        max_length=20,
        choices=BILLING_CYCLES,
        default='monthly',
    )

    amount = models.DecimalField(
        'subscription price',
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )

    currency = models.CharField(
        'currency',
        max_length=10,
        default='BDT',
    )

    started_at = models.DateTimeField(
        'start date',
        default=timezone.now,
    )

    expires_at = models.DateTimeField(
        'expiry date',
    )

    is_active = models.BooleanField(
        'active status',
        default=True,
    )

    warning_notified = models.BooleanField(
        '7-day warning sent',
        default=False,
        help_text='True if the 7-day expiration reminder notification has already been triggered',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.user.email} — {self.plan_display_name} ({self.status_display})"

    @property
    def is_expired(self):
        """Check if current subscription has passed its expiration date."""
        return timezone.now() > self.expires_at

    @property
    def days_remaining(self):
        """Calculate remaining days until expiration."""
        if self.is_expired:
            return 0
        delta = self.expires_at - timezone.now()
        return max(0, delta.days)

    @property
    def is_expiring_soon(self):
        """Check if subscription expires within the next 7 days."""
        if self.is_expired:
            return False
        return self.days_remaining <= 7

    @property
    def status_display(self):
        """Return human-readable status badge class and text."""
        if self.is_expired or not self.is_active:
            return 'Expired'
        elif self.is_expiring_soon:
            return f'Expiring Soon ({self.days_remaining}d left)'
        return 'Active'

    @property
    def status_badge_class(self):
        if self.is_expired or not self.is_active:
            return 'danger'
        elif self.is_expiring_soon:
            return 'warning'
        return 'success'


class PaymentTransaction(models.Model):
    """
    Records payment gateway transaction receipts (bKash, Nagad, Upay, Credit/Debit Card).
    """

    METHOD_CHOICES = [
        ('bkash', 'bKash Mobile Banking'),
        ('nagad', 'Nagad Mobile Banking'),
        ('upay', 'Upay Mobile Banking'),
        ('card', 'Credit / Debit Card'),
    ]

    STATUS_CHOICES = [
        ('completed', 'Completed & Verified'),
        ('pending', 'Pending Verification'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='payment_transactions',
        verbose_name='payer',
    )

    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions',
        verbose_name='associated subscription',
    )

    transaction_id = models.CharField(
        'transaction ID',
        max_length=64,
        unique=True,
        help_text='Unique identifier e.g. TXN-BKASH-894120',
    )

    payment_method = models.CharField(
        'payment method',
        max_length=20,
        choices=METHOD_CHOICES,
    )

    account_number = models.CharField(
        'account / card number',
        max_length=50,
        blank=True,
        help_text='Masked account or card digits e.g. 017****9201 or **** 4242',
    )

    amount = models.DecimalField(
        'amount paid',
        max_digits=10,
        decimal_places=2,
    )

    currency = models.CharField(
        'currency',
        max_length=10,
        default='BDT',
    )

    status = models.CharField(
        'status',
        max_length=20,
        choices=STATUS_CHOICES,
        default='completed',
    )

    created_at = models.DateTimeField('transaction timestamp', auto_now_add=True)

    class Meta:
        verbose_name = 'Payment Transaction'
        verbose_name_plural = 'Payment Transactions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.transaction_id} — {self.get_payment_method_display()} ({self.amount} {self.currency})"
