# 01. Defense Overview, Pitch Script & Core Cheatsheet

---

## 🎯 1. 5-Minute Defense Speech (Presentation Script)

Use this script during the first 3-5 minutes of your defense presentation to give the viva board a professional, structured overview of InternAI.

### 🎙️ English Version
> "Respected Teachers and Board Members, welcome to my Practicum Final Defense. Today, I am presenting **InternAI** — an AI-Powered Internship Management & Recruitment Ecosystem.
> 
> **Problem Statement:** Traditional internship placement processes rely on fragmented emails, manual resume screening, and informal communication. Recruiters struggle to filter qualified candidates, students lack feedback on their resumes, and academic supervisors face difficulty tracking weekly student progress during internships.
> 
> **Our Solution:** InternAI bridges this gap by unifying four distinct user stakeholders into a single platform:
> 1. **Students:** Who browse internships, receive AI skill match scores on their PDF resumes, auto-generate AI cover letters, and log weekly reports.
> 2. **Companies (Recruiters):** Who manage a 7-stage ATS (Applicant Tracking System) recruitment pipeline, schedule interviews, and evaluate top AI-ranked talent.
> 3. **Academic Supervisors:** Who monitor student internship attendance, grade weekly logs, and complete final evaluations.
> 4. **Administrators:** Who moderate users, verify company credentials, and approve internship listings.
> 
> **Tech Stack:** Built with **Django 5 (Python 3.12)** on the backend, **MySQL** for database management, **Groq Cloud API (Llama 3.3 70B)** for AI resume parsing & match scoring, and **Bootstrap 5.3 + Chart.js** for a responsive frontend dashboard. Thank you, and I am now ready for your questions and live demonstration."

---

### 🎙️ Bengali Version (বাংলা সংস্করণ - প্রেজেন্টেশনের জন্য)
> "শ্রদ্ধেয় স্যার ও ম্যাম, আমার প্র্যাকটিক্যাম ফাইনাল ডিফেন্সে আপনাকে স্বাগতম। আজকে আমি উপস্থাপন করছি **InternAI** — একটি AI-চালিত ইন্টার্নশিপ ম্যানেজমেন্ট এবং রিক্রুটমেন্ট প্ল্যাটফর্ম।
> 
> **মূল সমস্যা (Problem):** এনালগ বা ম্যানুয়াল সিস্টেমে ইন্টার্নশিপের আবেদন, সিভি বা রেজুমে স্ক্রিনিং, ইন্টারভিউ সিডিউলিং এবং ইন্টার্নদের সাপ্তাহিক রিপোর্টিং ট্র্যাকিং করা খুবই জটিল এবং সময়সাপেক্ষ।
> 
> **আমাদের সমাধান (Solution):** InternAI এই সমস্যা সমাধান করতে ৪টি রোলকে একটি প্ল্যাটফর্মে নিয়ে এসেছে:
> ১. **স্টুডেন্ট (Student):** যারা ইন্টার্নশিপ ব্রাউজ করতে পারে, সিভি আপলোড করলে AI দিয়ে Skill Match Score (০-১০০%) দেখতে পায়, AI Cover Letter জেনারেট করতে পারে এবং সাপ্তাহিক রিপোর্ট জমা দিতে পারে।
> ২. **কোম্পানি (Company/Recruiter):** যারা ৭-স্টেজের ATS (Applicant Tracking System) পাইপলাইনের মাধ্যমে ক্যান্ডিডেট শর্টলিস্ট, ইন্টারভিউ সিডিউল এবং অফার লেটার পাঠাতে পারে।
> ৩. **সুপারভাইজার (Academic Supervisor):** যারা স্টুডেন্টদের প্রতি সপ্তাহের কাজের রিপোর্ট গ্রেডিং করেন এবং ফাইনাল এভালুয়েশন ফর্ম পূরণ করেন।
> ৪. **এডমিন (Admin):** যারা কোম্পানি ভেরিফিকেশন, ইউজার মডারেশন এবং নতুন পোস্ট এপ্রুভ করেন।
> 
> **টেকনোলজি স্ট্যাক:** প্রজেক্টটি ব্যাকএন্ডে **Django 5 (Python 3.12)**, ডাটাবেজে **MySQL**, রেজুমে পার্সিং ও AI স্কোরিংয়ে **Groq Cloud API (Llama 3.3 70B Model)** এবং ফ্রন্টএন্ডে **Bootstrap 5.3 ও Chart.js** দিয়ে তৈরি করা হয়েছে।"

---

## 💡 2. Core Django Concepts (Viva Board Crash Course)

### 2.1 Django MVT Architecture (Model-View-Template)
- **Question:** What is MVT in Django and how does it differ from traditional MVC?
- **Answer (English):** Django uses **MVT (Model-View-Template)**.
  - **Model:** Python classes in `models.py` that map directly to database tables via Django ORM.
  - **View:** Python functions or classes in `views.py` that contain business logic, process request data, interact with Models, and render Templates. (Acts like the Controller in traditional MVC).
  - **Template:** HTML files in `templates/` mixed with Django Template Language (DTL) tags (`{% %}` and `{{ }}`) to render dynamic UI. (Acts like the View in traditional MVC).
- **সহজ বাংলা ব্যাখ্যা:** Django-তে MVC এর বদলে MVT বলা হয়। 
  - `Model` ডাটাবেজ টেবিল হ্যান্ডেল করে।
  - `View` বিজনেজ লজিক প্রসেস করে ডাটাবেজ থেকে ডাটা নিয়ে টেমপ্লেটে পাঠায় (Controller এর কাজ করে)।
  - `Template` হলো HTML পেজ যেখানে ডাইনামিক ডাটা দেখানো হয়।

```
[Browser Request] ──> [urls.py] ──> [views.py (Logic)] <──> [models.py (Database)]
                                        │
                                        ▼
                              [Template (HTML)] ──> [Browser Response]
```

---

### 2.2 Decorators & Access Control
- **Question:** What does `@login_required` mean? How are role permissions enforced?
- **Answer:** 
  - A **Decorator** in Python is a function that wraps another function to extend its behavior without modifying its code.
  - `@login_required` checks if `request.user.is_authenticated` is True. If False, it intercepts the request and redirects the user to `/accounts/login/`.
  - **Role Decorators in InternAI (`common/decorators.py`):** We created custom decorators `@student_required`, `@company_required`, and `@supervisor_required` using `@user_passes_test(lambda u: u.role == 'student')`.
- **বাংলা ব্যাখ্যা:** ডেকোরেটর (যেমন `@login_required`) হলো একটি পাইথন ফাংশন যা অন্য কোনো ভিউ ফাংশনের উপরে বসিয়ে দেয়া হয়। এটি চেক করে ইউজার লগইন করা আছে কিনা। লগইন না থাকলে সরাসরি লগইন পেজে রিডাইরেক্ট করে দেয়।

```python
# Code example from common/decorators.py
from django.contrib.auth.decorators import user_passes_test

def student_required(view_func):
    # Restricts access to Student users only
    decorated_view_func = user_passes_test(
        lambda u: u.is_authenticated and u.role == 'student',
        login_url='accounts:login'
    )
    return decorated_view_func(view_func)
```

---

### 2.3 URL Routing & Parameter Passing
- **Question:** How does `path('internship/<int:pk>/', views.internship_detail, name='detail')` work?
- **Answer:**
  - `path()` registers a URL endpoint.
  - `<int:pk>` is a **Path Converter**. It captures an integer value from the URL (e.g. `/internship/5/`) and passes it as a keyword argument named `pk=5` into the view function `internship_detail(request, pk)`.
  - `name='detail'` allows generating dynamic URLs in templates using `{% url 'internships:detail' internship.id %}` or in Python views using `reverse('internships:detail', args=[pk])`.

---

### 2.4 Django ORM & Database Relationships
- **Question:** What is Django ORM and what relationship types are used in InternAI?
- **Answer:**
  - **ORM (Object-Relational Mapper):** Allows manipulating database tables using Python objects without writing raw SQL.
  - **Relationships in InternAI (`models.py`):**
    1. **`OneToOneField`:** Used in `StudentProfile(user=OneToOneField(CustomUser))` — One User has exactly One Profile.
    2. **`ForeignKey` (1-to-Many):** Used in `Application(student=ForeignKey(CustomUser), internship=ForeignKey(Internship))` — One Student can submit multiple Applications; One Internship can receive multiple Applications.
    3. **`ManyToManyField` (Many-to-Many):** Used in `Conversation(participants=ManyToManyField(CustomUser))` — A conversation thread can have multiple users participating.
  - **`on_delete=models.CASCADE`:** When the parent object (e.g., User) is deleted, all associated child objects (e.g., StudentProfile, Applications) are automatically deleted.
  - **`on_delete=models.SET_NULL`:** Keeps child record but sets FK column to NULL (used when retaining history).

---

### 2.5 Security & Environment Variables
- **Question:** How are passwords and API keys secured in InternAI?
- **Answer:**
  - **Password Security:** Django automatically hashes passwords using **PBKDF2 with SHA-256** algorithm before saving to `CustomUser.password`. Raw passwords are NEVER stored in cleartext.
  - **CSRF Protection:** Forms include `{% csrf_token %}` which embeds a secret, cryptographically signed token to prevent Cross-Site Request Forgery attacks.
  - **Secrets Isolation:** Sensitive keys (`SECRET_KEY`, `GROQ_API_KEY`, `STRIPE_SECRET_KEY`, Database credentials) are stored in the `.env` file and parsed with `python-dotenv` in `internai/settings.py`. `.env` is listed in `.gitignore` to prevent leaking keys in version control.
