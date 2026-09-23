# 07. Practicum Defense Board Question & Answer Handbook (InternAI)

> **Document Purpose:** Complete, step-by-step model answers for real Practicum Defense Board Viva & Live Coding questions for **InternAI**.  
> **Language:** Bengali & English (Bilingual for viva presentation).

---

## 📋 Table of Contents
1. [Question 1: Project Idea & Problem Statement (Ki Problem Solve Kortechen?)](#1-project-idea--problem-statement)
2. [Question 2: Feature Selection & Rationale (Kon Jukti Te Feature Select Korechen?)](#2-feature-selection--rationale)
3. [Question 3: Input Validation Mechanics & Live Addition (Input Validation Check & Live Add)](#3-input-validation-mechanics--live-addition)
4. [Question 4: URL Routing & Request Dispatching (Routing Dekhate Bolbe)](#4-url-routing--request-dispatching)
5. [Question 5: Button Action Triggers & Form Submissions (Button Kivabe Perform Kore)](#5-button-action-triggers--form-submissions)
6. [Question 6: Live Form Field Addition & Deletion (Field Barano / Delete Kora)](#6-live-form-field-addition--deletion)
7. [Question 7: PDF Export & Ascending / Descending Sorting (PDF Print & Order By)](#7-pdf-export--ascending--descending-sorting)
8. [Question 8: Payment Gateway & Billing Mechanics (Payment Method Kivabe Kaj Kore)](#8-payment-gateway--billing-mechanics)

---

## 🎯 1. Project Idea & Problem Statement

### ❓ Question from Board:
*"Apnar project er main idea ki? Eta kon specific real-world problem solve kortoche?"*  
*(What is the core idea of your project, and what specific problem does it solve?)*

### 🗣️ Model Answer (Bengali Presentation):
> "Sir, **InternAI** holo ekti AI-Powered Internship Management & Recruitment Platform. 
> Traditional systemic-e internship khunja ebong hiring process fragmented ebong manual.
> 
> **Amader Platform specific 4 ti problem solve korche:**
> 1. **Student Problem:** Students blind-ly multiple internships-e apply kore, kintu tara jaane na tader Resume job requirement er sathe kototuki match korche. Plus, resume manual parsing-e somoy jai.
> 2. **Company / HR Problem:** Hundreds of PDF resume manually screen kora HR-er jonno osombhob somoy shapokkho. InternAI-er **Groq Llama 3.3 70B AI Match Engine** automatic PDF parse kore candidate profile-er sathe match percentage (0-100%) score ebong skill gap feedback produce kore.
> 3. **Academic Supervisor Problem:** University-er practicum course-e supervisors student-der weekly report, attendance, and performance track korte paren na. InternAI-te dedicated Supervisor portal-e digital mid-term & final evaluation form royeche.
> 4. **Placement Office / Admin Problem:** University or Admin clear access paay na kon student kothay placed holo ebong company verification fake kina. InternAI-te Admin complete subscription, placement tracking, and company verification control korte pare."

### 💻 Code & File References:
- **AI Matching Engine:** `common/ai_engine.py` -> `calculate_skill_match()`
- **Multi-Role User Routing:** `accounts/models.py` -> `User.Role` (`STUDENT`, `COMPANY`, `SUPERVISOR`, `ADMIN`)

---

## 💡 2. Feature Selection & Rationale

### ❓ Question from Board:
*"Project er feature gulo keno select korechen? Kon jukti te egula add kora hoyeche?"*  
*(Why did you choose these specific features? What is the logic behind selecting them?)*

### 🗣️ Model Answer (Bengali Presentation):
> "Sir, amra protekta feature specific business logic & user workflow problem solve korar jukttite select korechi:
> 
> 1. **AI Resume & Job Match Scoring (Groq AI):**
>    - *Jukti:* HR candidate screening time 90% komate ebong student-der target skill gap bujhte help korte.
> 2. **Subscription Tier Limits (Basic vs Boost vs Ultimate):**
>    - *Jukti:* Spam application rokka korte. Basic plan-er student high-volume spam application korte parbe na (max 10 apps/month). Boost/Ultimate users parbe 50+ apps apply korte. System monetization audit-er sathe match kore.
> 3. **Company Verification & Admin Account Suspension:**
>    - *Jukti:* Fake company scam internships theke student-der surokkhit rakhar jonno Admin company verify o suspend korte pare (`is_active=False`), shaathe shaathe post stop hoye jaabe.
> 4. **Academic Supervisor Linkage & Digital Evaluation:**
>    - *Jukti:* University practicum course requirements complete korar jonno official supervisor digital grade submit korte pare.
> 5. **Real-time Messaging & Notification System:**
>    - *Jukti:* Email loss avoid kore applicant o company recruiters-er majhe immediate interview updates o status updates pathate."

---

## 🔒 3. Input Validation Mechanics & Live Addition

### ❓ Question from Board:
*"Apnar project-e input validation kivabe check hochhe? Validation na thakle ekhoni add kore dekhann."*  
*(How is input validation handled? If validation is missing for a field, add it live now.)*

### 🗣️ Model Answer (Explanation):
InternAI implements a **3-Layer Security & Validation System**:
1. **Frontend Validation:** HTML5 attributes (`required`, `type="email"`, `min="0.0"`, `max="4.0"`, `step="0.01"`).
2. **Form / Model Level Validation:** Django Model Field Validators (`MinValueValidator`, `MaxValueValidator`, `FileExtensionValidator(['pdf'])`).
3. **View-Level Business Logic Checks:** Checks application limits, GPA requirements, active company status, and duplicate submission checks.

### 🛠️ Live Defense Modification Demo (On the Spot):
If the board asks: *"Add validation so GPA cannot be less than 3.0 when applying for an internship!"*

Open `applications/views.py` inside `submit()` function and edit lines 25-28:

```python
# Live Validation Check Addition:
student_profile = get_object_or_404(StudentProfile, user=request.user)

if student_profile.gpa and student_profile.gpa < 3.0:
    messages.error(request, "Minimum GPA requirement of 3.0 is required to apply.")
    return redirect('internships:detail', pk=internship.id)
```

If the board asks for **Form Field Validation** in `forms.py`:

```python
from django import forms
from django.core.exceptions import ValidationError

class StudentProfileForm(forms.ModelForm):
    # Live Field Validation Example:
    def clean_gpa(self):
        gpa = self.cleaned_data.get('gpa')
        if gpa is not None and (gpa < 0.0 or gpa > 4.0):
            raise ValidationError("GPA must be between 0.00 and 4.00")
        return gpa
```

---

## 🛣️ 4. URL Routing & Request Dispatching

### ❓ Question from Board:
*"Routing gulo dekhann. Ekta URL hit korle request kivabe view porjonto pouchai?"*  
*(Show us the routing. When a URL is accessed, how does the request reach the view?)*

### 🗣️ Model Answer (Explanation):
> "Sir, Django hierarchical routing pattern follow kore:
> 1. Browser initial URL hit kore (e.g. `http://localhost:8000/applications/submit/5/`).
> 2. Project-er Main Root URL file `internai/urls.py`-te request aase. Prefix `/applications/` dekhe dispatch kore `applications.urls`-e.
> 3. App-level `applications/urls.py` file-e URL path pattern match kore:
>    `path('submit/<int:internship_id>/', views.submit, name='submit')`
> 4. Dynamic URL parameter `internship_id=5` parse hoye View function `applications.views.submit(request, internship_id=5)`-e chole jaay.
> 5. View function logic process kore Template return kore athoba Redirect keyword use kore response back kore."

### 💻 Code Structure to Show Board:
- **Root Routing (`internai/urls.py`):**
  ```python
  path('applications/', include('applications.urls', namespace='applications')),
  path('internships/', include('internships.urls', namespace='internships')),
  path('billing/', include('billing.urls', namespace='billing')),
  ```
- **App Routing (`applications/urls.py`):**
  ```python
  app_name = 'applications'
  urlpatterns = [
      path('submit/<int:internship_id>/', views.submit, name='submit'),
      path('my-applications/', views.my_applications, name='my_applications'),
  ]
  ```

---

## 🔘 5. Button Action Triggers & Form Submissions

### ❓ Question from Board:
*"Web page-er Button gulo kivabe perform kore? Action trigger kinetic ki ghotteche?"*  
*(How do buttons perform actions? What happens when a button is clicked?)*

### 🗣️ Model Answer (Explanation):
InternAI-te button-gulo **2 bhabe perform kore**:

#### Type A: Synchronous HTML Form Buttons (Submit & Redirect)
1. User click kore: `<button type="submit" class="btn btn-primary">Submit Application</button>`
2. Form attribute POST method pathae: `<form method="POST" action="{% url 'applications:submit' internship.id %}">`
3. Hidden CSRF Token `<input type="hidden" name="csrfmiddlewaretoken" value="...">` request-er shaathe cross-site forgery check complete kore.
4. View file-e check hoy `if request.method == 'POST':`. View data process kore DB-te save kore (`application.save()`), success alert create kore (`messages.success(...)`), and HTTP 302 Redirect return kore (`return redirect('internships:detail', pk=internship.pk)`).

#### Type B: Asynchronous AJAX Buttons (JavaScript & API Fetch)
1. Example: **AI Match Score Calculator Button** in `internships/detail.html`.
2. Button click handle kore Vanilla JS event listener:
   ```javascript
   document.getElementById('ai-match-btn').addEventListener('click', async function() {
       const response = await fetch('/applications/api/calculate-match/', {
           method: 'POST',
           headers: {'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json'},
           body: JSON.stringify({ internship_id: 5 })
       });
       const data = await response.json();
       document.getElementById('match-score-display').innerText = data.score + '%';
   });
   ```
3. Dynamic DOM update hoy, kono page reload hoy na.

---

## ✏️ 6. Live Form Field Addition & Deletion

### ❓ Question from Board:
*"Ekta form-e on-the-spot farokt field add athoba delete kore dekhann."*  
*(Add or delete a field from a form live on the spot.)*

### 🛠️ Live Defense Step-by-Step Procedure:

#### Example: Adding `phone_number` field to `StudentProfile`
1. **Open `models.py` (e.g. `students/models.py`):**
   ```python
   # Add new field:
   phone_number = models.CharField(max_length=20, blank=True, null=True)
   ```
2. **Run Migrations in Terminal:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. **Update Form in `forms.py` (e.g. `students/forms.py`):**
   ```python
   class StudentProfileForm(forms.ModelForm):
       class Meta:
           model = StudentProfile
           fields = ['full_name', 'phone_number', 'gpa', 'university', 'resume_file']
   ```
4. **Update Template HTML:**
   ```html
   <div class="mb-3">
       <label for="id_phone_number" class="form-label">Phone Number</label>
       {{ form.phone_number }}
   </div>
   ```

#### Deleting a Field:
- Reverse the steps: Comment out/remove field from `fields` list in `forms.py`, remove input element from HTML template, and optionally drop column from model and run migrations.

---

## 📄 7. PDF Export & Ascending / Descending Sorting

### ❓ Question from Board:
*"Apnar system-e PDF print option ache? Data Ascending or Descending order-e sorting kivabe kora hoyeche?"*  
*(Does your system have a PDF print option? How is sorting handled in Ascending vs Descending order?)*

### 🗣️ Model Answer (Explanation):
> "Sir, amader system-e **Report & Analytics module**-e PDF Generation module royeche. Views HTML template context render kore PDF response header output kore (`HttpResponse(content_type='application/pdf')`)."

### 🔄 Sorting Logic (Ascending vs Descending Order):
Sorting handle kora hoy Django ORM `order_by()` method ebong GET Query parameters die:

```python
# reports/views.py or applications/views.py
def generate_application_report_pdf(request):
    # Get sort parameters from URL query string (e.g., ?sort=gpa&order=desc)
    sort_field = request.GET.get('sort', 'created_at')  # Default sorting field
    order_direction = request.GET.get('order', 'desc')  # Default direction
    
    # Check direction and construct ORM field lookup
    if order_direction == 'desc':
        ordering = f"-{sort_field}"  # Descending: Highest to lowest / Z-A / Newest first
    else:
        ordering = sort_field       # Ascending: Lowest to highest / A-Z / Oldest first

    # Query database with dynamic sorting
    applications = Application.objects.filter(status='accepted').order_by(ordering)
    
    # Render to PDF
    # ... PDF rendering logic ...
```

#### 📊 Quick Ascending vs Descending Cheatsheet:
| Order Type | Django ORM Syntax | Real Example | Outcome |
| :--- | :--- | :--- | :--- |
| **Ascending (Lowest -> Highest)** | `.order_by('created_at')` | Oldest applications first | 1 Jan -> 31 Dec |
| **Descending (Highest -> Lowest)** | `.order_by('-created_at')` | Newest applications first | 31 Dec -> 1 Jan |
| **GPA Ascending** | `.order_by('student__gpa')` | Lowest GPA first | 2.5 -> 4.0 |
| **GPA Descending** | `.order_by('-student__gpa')` | Highest GPA first | 4.0 -> 2.5 |
| **AI Match Score Descending** | `.order_by('-match_score')` | Best matched candidates on top | 95% -> 40% |

---

## 💳 8. Payment Gateway & Billing Mechanics

### ❓ Question from Board:
*"Payment method o billing tier system kivabe kaj kortoche?"*  
*(How does the payment method and billing system work?)*

### 🗣️ Model Answer (Explanation):
> "Sir, InternAI-te **Billing & Subscription App** royeche. Eta student o company-der tier-based features o application quota manage kore.
> 
> **End-to-End Payment Workflow:**
> 1. **Plan Selection:** Student `/billing/plans/`-e giye 'Student Boost Plan' (৳500/mo) click kore.
> 2. **Pending Transaction Creation:** System DB-te `Subscription` record status='pending' and `PaymentTransaction` create kore unique Transaction ID shoho (`trx_id = 'TXN-998821'`).
> 3. **Gateway Initiation (SSLCommerz / Sandbox Gateway):** View function payment gateway API endpoint-e payload pathae (`store_id`, `amount`, `currency='BDT'`, `tran_id`, `success_url`, `cancel_url`).
> 4. **User Gateway Payment:** User-ke SSLCommerz / bKash / Nagad / Card payment portal-e redirect kora hoy.
> 5. **Callback Verification & IPN:** Payment complete hole gateway system-er `payment_success` callback view-e response POST kore. View digital hash signature check kore transaction verify kore.
> 6. **Subscription Activation & Limit Update:** View `Subscription.status = 'active'` update kore. Application module-e user-er `max_allowed` monthly limit 10-tier overall auto-increment hoye 50-te porinoto hoy."

### 💻 Database Models (`billing/models.py`):
```python
class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100) # Basic, Boost, Ultimate
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_applications = models.IntegerField(default=10)
    ai_resume_builder_access = models.BooleanField(default=False)

class PaymentTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('PENDING', 'Pending'), ('SUCCESS', 'Success'), ('FAILED', 'Failed')])
    created_at = models.DateTimeField(auto_now_add=True)
```

---

## 🏁 Summary Checklist for Practical Defense
- [x] Know how to pitch **InternAI** in 2 minutes.
- [x] Know how to explain **Groq AI Match Engine**.
- [x] Know how to edit `applications/views.py` live to add GPA validation.
- [x] Know how to explain Django `urls.py` routing dispatch.
- [x] Know how HTML form buttons vs AJAX buttons operate.
- [x] Know how to add/remove form fields in Model, Form & Template.
- [x] Know how `.order_by('-field')` handles Descending order in PDF reports.
- [x] Know how SSLCommerz Payment callback updates subscription tier limits.
