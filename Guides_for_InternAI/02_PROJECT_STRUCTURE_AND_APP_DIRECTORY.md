# 02. Project Structure & 16-App Directory Guide

---

## 📂 1. Directory Tree Map

```
InternAi/
├── internai/                # Core Django Config (settings.py, urls.py, wsgi.py)
├── accounts/                # User Authentication, Registration & 3 Profiles
├── internships/             # Internship Postings, Categories & Bookmarks
├── applications/            # Application Submission, ATS Status Pipeline & AI Cover Letter
├── interviews/              # Interview Scheduling & Meeting Links
├── reports/                 # Weekly Activity Logs & Supervisor Evaluations
├── analytics/               # Role-Specific Dashboards (Chart.js Integration)
├── chatbot/                 # AI Assistant (Groq Cloud LLM, Session History & Floating Widget)
├── messaging/               # Internal Threaded Messaging System
├── notifications/           # Real-Time In-App Alerts & Counters
├── billing/                 # Stripe Subscriptions & Pricing Plans
├── documents/               # File Storage & Audit Log Auditing
├── administration/          # Admin Portal (User Moderation, Company Verification, Post Approval)
├── common/                  # Core Utilities (ai_engine.py, context_processors.py, decorators.py)
├── static/                  # CSS Stylesheets, JS Files, Images
├── templates/               # Shared HTML Layouts (base.html, sidebar.html)
├── manage.py                # Django Command-Line Utility
└── .env                     # Secret Key & API Configurations
```

---

## 🏢 2. Deep-Dive into Each Django App

### 1. `internai` (Core Configuration)
- **`settings.py`**: Configures installed apps, database credentials, authentication user model (`AUTH_USER_MODEL = 'accounts.CustomUser'`), Groq API key, media paths, and global context processors.
- **`urls.py`**: Master URL Router. Delegates URL sub-paths to individual apps using `include()`.
  ```python
  path('accounts/', include('accounts.urls')),
  path('internships/', include('internships.urls')),
  path('applications/', include('applications.urls')),
  # ... other app inclusions
  ```

---

### 2. `accounts` (Authentication & Profiles)
- **Key Models (`accounts/models.py`):**
  - `CustomUser`: Inherits `AbstractUser`. Stores `email`, `role` (`student`, `company`, `supervisor`, `admin`), `phone`, `avatar`.
  - `StudentProfile`: Stores `university`, `department`, `gpa`, `skills`, `github_url`, `linkedin_url`, `portfolio_url`.
  - `CompanyProfile`: Stores `company_name`, `industry`, `logo`, `is_verified`, `subscription_plan`.
  - `SupervisorProfile`: Stores `designation`, `expertise`, `max_students`.
- **Key Views (`accounts/views.py`):**
  - `register_view()`: Handles role selection & account creation.
  - `login_view()`: Authenticates user credentials and redirects to role-specific dashboard.
  - `logout_view()`: Destroys session and redirects to landing page.
  - `profile_edit_view()`: Allows updating profile information & avatar.

---

### 3. `internships` (Postings & Bookmarks)
- **Key Models (`internships/models.py`):**
  - `InternshipCategory`: Predefined categories (Software Engineering, Data Science, Cyber Security, etc.).
  - `Internship`: Job listing table containing `title`, `description`, `requirements`, `skills_required`, `internship_type` (Onsite, Remote, Hybrid), `stipend`, `deadline`, `status` (`open`, `closed`), `is_approved`.
  - `SavedInternship`: Bookmark junction table for students (`unique_together = ('student', 'internship')`).
- **Key Views (`internships/views.py`):**
  - `internship_list()`: Search engine supporting filter by search query, category, type, and location.
  - `internship_detail()`: Displays full job description, requirements, and "Apply Now" button.
  - `internship_create()`: Allows verified companies to post new positions.
  - `toggle_save()`: AJAX endpoint to bookmark/unbookmark an internship.

---

### 4. `applications` (ATS Pipeline & AI Engine Interface)
- **Key Models (`applications/models.py`):**
  - `Application`: Tracks student job application with fields `student`, `internship`, `status` (`pending`, `reviewing`, `assessment`, `interview`, `offer`, `accepted`, `rejected`), `cover_letter`, `resume`, `ai_match_score` (0-100%).
- **Key Views (`applications/views.py`):**
  - `submit_application()`: Processes PDF resume upload, extracts text using `pypdf`, triggers AI match scoring via `common/ai_engine.py`, and creates `Application` record.
  - `update_status()`: Recruiter view to move candidate across 7 ATS pipeline stages.
  - `generate_ai_cover_letter_api()`: AJAX endpoint calling Groq LLM to draft a cover letter.

---

### 5. `chatbot` (AI Assistant & Floating Widget)
- **Key Models (`chatbot/models.py`):**
  - `ChatSession`: Represents a chat thread for a user.
  - `ChatMessage`: Individual message record (`session`, `role` (`user`/`assistant`), `content`, `timestamp`).
- **Key Views (`chatbot/views.py`):**
  - `chat_api()`: AJAX endpoint that processes user prompt, prepends a system prompt tailored to user role, sends payload to **Groq Cloud API (Llama 3.3 70B)**, saves assistant response to database, and returns JSON.
  - `floating_widget.html`: Included globally in `templates/base.html` so students can ask questions anywhere on the platform.

---

### 6. `analytics` (Visual Intelligence & Dashboards)
- **Key Views (`analytics/views.py`):**
  - Aggregate DB queries using Django `Count`, `Avg`, `TruncMonth`.
  - Passes structured JSON data to templates for **Chart.js** rendering.
  - Separate views for `student_analytics`, `company_analytics`, `supervisor_analytics`, `admin_analytics`.

---

### 7. `reports` & `interviews` (Monitoring & Scheduling)
- `reports/models.py`: `WeeklyReport` (submitted by students), `Evaluation` (graded by supervisors with scores 0-100).
- `interviews/models.py`: `Interview` (scheduled by companies, includes Google Meet/Zoom link, date/time, and status).

---

### 8. `common` (Core Engine & Context Processors)
- `common/ai_engine.py`: PDF parser (`extract_text_from_pdf`) and Groq AI Skill Matcher (`calculate_skill_match`).
- `common/context_processors.py`: Provides global variables `unread_notifications_count` and `unread_messages_count` to all templates for live sidebar badges.
- `common/decorators.py`: Custom role-based security access functions.
