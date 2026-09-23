# InternAI - Payment Architecture & Form Customization Master Guide

This document provides a comprehensive technical breakdown of how the payment/billing system works in **InternAI** (including bKash, Nagad, Upay, and Cards) and provides a step-by-step tutorial on adding or deleting form fields in Django.

---

## 1. Payment Gateway & Subscription Architecture

The billing system in InternAI (`billing/` app) handles monetized access for recruiting companies and premium student career plans. It supports Bangladeshi Mobile Financial Services (MFS) as well as Credit/Debit card transactions.

### A. Core Database Models (`billing/models.py`)

1. **`Subscription` Model**:
   - Tracks active and past plans (e.g., `Pro Recruiter Plan`, `Student Career Boost`).
   - Fields: `user`, `plan_name`, `amount`, `currency` (default: BDT), `started_at`, `expires_at`, `is_active`, `warning_notified` (7-day warning state).
   - Helper properties: `is_expired`, `days_remaining`, `is_expiring_soon`, `status_badge_class`.

2. **`PaymentTransaction` Model**:
   - Records transaction receipts and audit trail.
   - Fields: `user`, `subscription`, `transaction_id` (e.g. `TXN-BKASH-894120`), `payment_method` (`bkash`, `nagad`, `upay`, `card`), `account_number`, `amount`, `status` (`completed`, `pending`, `failed`, `refunded`).

---

### B. Supported Payment Channels

| Payment Channel | Method Code | Account Input Format | Transaction Verification Process |
| :--- | :--- | :--- | :--- |
| **bKash Mobile Banking** | `bkash` | `017XXXXXXXX` | PIN + OTP verification simulation & hash ID generation. |
| **Nagad Mobile Banking** | `nagad` | `018XXXXXXXX` | Automated gateway callback simulation. |
| **Upay Mobile Banking** | `upay` | `019XXXXXXXX` | Instant wallet transaction receipt log. |
| **Credit / Debit Card** | `card` | `**** 4242` | Stripe / SSLCommerz sandbox token validation. |

---

### C. End-to-End Payment Transaction Flow

```
[ Plan Selection ] -> [ Checkout Form ] -> [ Payment Processing View ] -> [ DB Transaction Created ] -> [ Subscription Extended ]
```

#### Backend Transaction Handler (`billing/views.py`)
```python
@login_required
def process_checkout(request):
    if request.method == 'POST':
        plan_name = request.POST.get('plan_name')
        method = request.POST.get('payment_method')
        amount = request.POST.get('amount')
        
        # 1. Create Payment Transaction Log
        txn = PaymentTransaction.objects.create(
            user=request.user,
            transaction_id=f"TXN-{method.upper()}-{uuid.uuid4().hex[:8].upper()}",
            payment_method=method,
            amount=amount,
            status='completed'
        )
        
        # 2. Activate or Extend User Subscription
        sub, created = Subscription.objects.get_or_create(user=request.user)
        sub.plan_name = plan_name
        sub.expires_at = timezone.now() + timedelta(days=30)
        sub.is_active = True
        sub.save()
        
        messages.success(request, 'Payment successful! Subscription activated.')
        return redirect('billing:receipt', txn_id=txn.transaction_id)
```

---

## 2. Tutorial: How to Add or Delete Form Fields in Django

Examiners frequently ask live customization questions like: *"Add a new field (e.g., LinkedIn URL or Portfolio Link) to this form"* or *"Remove a field from this form"*. Follow this 5-step blueprint:

### Blueprint A: Adding a New Field (`linkedin_url`) to Student Profile Form

#### Step 1: Update Database Model Schema (`accounts/models.py`)
```python
class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    university = models.CharField(max_length=150)
    # ADD NEW FIELD HERE:
    linkedin_url = models.URLField('LinkedIn Profile', blank=True, null=True)
```

#### Step 2: Run Database Migrations (Terminal)
```bash
python manage.py makemigrations accounts
python manage.py migrate
```

#### Step 3: Update Django Form Class (`accounts/forms.py`)
```python
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['university', 'major', 'gpa', 'linkedin_url']  # ADD FIELD HERE
        widgets = {
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/user'}),
        }
```

#### Step 4: Update HTML Form Template (`students/templates/profile_edit.html`)
```html
<div class="mb-3">
    <label for="id_linkedin_url" class="form-label">LinkedIn Profile URL</label>
    {{ form.linkedin_url }}
</div>
```

#### Step 5: Process Field Data in View (`students/views.py`)
When using Django `ModelForm`, `form.save()` handles saving automatically. For custom processing:
```python
if form.is_valid():
    linkedin_url = form.cleaned_data.get('linkedin_url')
    form.save()
```

---

### Blueprint B: Deleting an Existing Field from a Form

1. **Remove from Form Class (`forms.py`)**: Delete the target field name from `fields = [...]` list inside the form's `Meta` class.
2. **Remove from HTML Template (`template.html`)**: Remove the HTML `<div>` rendering `{{ form.field_name }}`.
3. **(Optional) Database Schema Removal**: Remove field from `models.py` and run `python manage.py makemigrations` followed by `python manage.py migrate`.
