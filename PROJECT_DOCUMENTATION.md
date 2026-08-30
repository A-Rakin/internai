# InternAI — Project Structure, Database Models & Business Logic

InternAI is an AI-powered Internship Management & Recruitment Ecosystem designed to streamline the recruitment, scheduling, evaluation, monitoring, and communication processes for student internships. It serves four distinct user roles: **Students**, **Companies (HR Recruiters)**, **Academic Supervisors**, and **Administrators**.

---

## 1. Project Architecture & Directory Structure

InternAI is built using **Django 5** (Python 3.12) on the backend, **Bootstrap 5.3**, **Chart.js 4**, and **Vanilla CSS/JS** on the frontend, and **MySQL** for database storage. It is structured into 16 modular Django apps.

```
InternAi/
├── internai/                # Core Configuration
│   ├── settings.py          # Installed apps, database, Stripe, and auth config
│   ├── urls.py              # Global URL router
│   └── wsgi.py              # WSGI entrypoint
├── accounts/                # User Auth & Role Profiles
│   ├── models.py            # CustomUser, StudentProfile, CompanyProfile, SupervisorProfile
│   ├── views.py             # Auth logic, password reset, profile editing
│   └── urls.py              # /accounts/ routing
├── internships/             # Internship Listings & Bookmarks
│   ├── models.py            # InternshipCategory, Internship, SavedInternship
│   ├── views.py             # Listing browse, detail, search engine
│   └── urls.py              # /internships/ routing
├── applications/            # Recruitment Pipeline & Submission
│   ├── models.py            # Application model (status tracking, cover letter, resume)
│   ├── views.py             # Submission, AI Cover Letter generator endpoint
│   └── urls.py              # /applications/ routing
├── interviews/              # Interview Scheduling & Prep
│   ├── models.py            # Interview model (types, modes, links, outcomes)
│   └── urls.py              # /interviews/ routing
├── reports/                 # Monitoring & Weekly Activity
│   ├── models.py            # WeeklyReport, Evaluation
│   └── urls.py              # /reports/ routing
├── analytics/               # Visual Analytics & Intelligence
│   ├── views.py             # Data aggregation for Admin, Student, Company, Supervisor
│   ├── templates/           # Role-specific dashboard layouts with Chart.js
│   └── urls.py              # /analytics/ routing
├── chatbot/                 # AI Assistant & Chatbot
│   ├── models.py            # ChatSession, ChatMessage
│   ├── views.py             # Groq LLM integration, role-aware prompts, session management
│   ├── templates/           # Full-page chat & floating widget components
│   └── urls.py              # /chatbot/ routing
├── messaging/               # Internal Direct Messaging
│   ├── models.py            # Conversation (M2M participants), Message
│   ├── views.py             # Inbox, threaded chat, compose message
│   ├── templates/           # Inbox, thread, and compose templates
│   └── urls.py              # /messages/ routing
├── notifications/           # In-App Notifications
│   ├── models.py            # Notification model (application updates, reminders)
│   └── urls.py              # /notifications/ routing
├── billing/                 # Stripe Subscriptions
│   ├── views.py             # Checkout session generation, plan updates
│   └── urls.py              # /billing/ routing
├── common/                  # AI Engine & Core Utilities
│   ├── ai_engine.py         # PyPDF parser, Groq LLM API, local NLP matchers
│   ├── context_processors.py# Unread notifications & unread messages counters
│   └── urls.py              # Public landing page routes
├── documents/               # File Storage & Audit Trail
│   ├── models.py            # Document model, ActivityLog auditing
│   └── urls.py              # /documents/ routing
├── administration/          # Admin Management Portal
│   ├── views.py             # User moderation, company verification, internship approval
│   └── urls.py              # /administration/ routing
├── static/                  # CSS stylesheets, JS scripts, images
└── templates/               # Shared HTML layouts & sidebar components
```

---

## 2. Database Models (Schema)

The platform implements **16 custom database models** across modules:

### 2.1 User Management (`accounts` App)
- **`CustomUser`**: Inherits from `AbstractUser`. Uses `email` as unique login credential.
  - `role`: Choices are `student`, `company`, `supervisor`, `admin`.
  - `phone`, `avatar`, `is_email_verified`.
- **`StudentProfile`**: One-to-One with `CustomUser`.
  - `university`, `department`, `student_id`, `gpa`, `education_level`, `skills`, `portfolio_url`, `github_url`, `linkedin_url`.
- **`CompanyProfile`**: One-to-One with `CustomUser`.
  - `company_name`, `logo`, `industry`, `company_size`, `website`, `description`, `is_verified`, `subscription_plan` (`basic`, `pro`, `ultimate`).
- **`SupervisorProfile`**: One-to-One with `CustomUser`.
  - `designation`, `expertise`, `max_students`.

### 2.2 Listings, Bookmarks & Applications (`internships` & `applications` Apps)
- **`InternshipCategory`**: Category classifications (Software Dev, Data Science, etc.).
- **`Internship`**: Position listing by a company.
  - `title`, `description`, `requirements`, `skills_required`, `internship_type` (`onsite`, `remote`, `hybrid`), `stipend`, `deadline`, `status` (`draft`, `open`, `closed`, `filled`), `is_approved`, `is_featured`, `views_count`.
- **`SavedInternship`**: Unique constraint `(student, internship)` for bookmarking positions.
- **`Application`**: Candidate application submission.
  - `student`, `internship`, `status` (`pending`, `reviewing`, `assessment`, `interview`, `offer`, `accepted`, `rejected`), `cover_letter`, `resume`, `ai_match_score` (0-100%).

### 2.3 AI Assistant & Messaging (`chatbot` & `messaging` Apps)
- **`ChatSession`**: Session between a user and AI assistant (`user`, `title`, `is_active`, timestamps).
- **`ChatMessage`**: Individual chat message (`session`, `role` (`user`/`assistant`), `content`, `created_at`).
- **`Conversation`**: Direct messaging thread between users (`participants` M2M, `subject`, timestamps).
- **`Message`**: Message inside a conversation (`conversation`, `sender`, `content`, `is_read`, `read_at`).

### 2.4 Monitoring, Assessment & System (`interviews`, `reports`, `notifications`, `documents`)
- **`Interview`**: Interview record (`application`, `interview_type`, `mode`, `scheduled_at`, `meeting_link`, `outcome`, `score`, `notes`).
- **`WeeklyReport`**: Weekly student log (`week_number`, `activities`, `challenges`, `next_week_plan`, `hours_worked`, `status`, `score`, `feedback`).
- **`Evaluation`**: Academic evaluation form (`technical_score`, `communication_score`, `professionalism_score`, `attendance_score`, `overall_score`, `comments`, `recommendation`).
- **`Notification`**: In-app message notification (`recipient`, `notification_type`, `title`, `message`, `link`, `is_read`).
- **`Document`**: File upload repository (`user`, `title`, `file_type`, `file`, `file_size`).
- **`ActivityLog`**: System audit trail (`user`, `action`, `description`, `ip_address`).

---

## 3. End-to-End Workflows & Business Logic

### 3.1 AI Resume Analysis & Cover Letter Generation
1. **Resume PDF Parsing**: `extract_text_from_pdf()` extracts plain text from uploaded resumes using `pypdf`.
2. **AI Skill Match Engine**: `calculate_skill_match()` uses **Groq Cloud AI (Llama 3.3 70B)** to compare candidate skills against internship requirements, returning a score (50-98%), matched skills, missing skills, and recruiter advice. If offline, `_local_skill_match()` executes regex keyword matching.
3. **AI Cover Letter Generator**: `generate_cover_letter()` synthesizes student profile details with internship criteria to auto-draft a tailored cover letter.

### 3.2 AI Chatbot & Floating Widget
1. **System Prompting**: Generates role-aware system prompts (e.g., student vs. company recruiter vs. supervisor context).
2. **Session Persistence**: Stores full chat history in `ChatSession` and `ChatMessage`.
3. **Floating Widget**: Global component included via `templates/base.html` allowing one-click access anywhere on the platform.

### 3.3 Advanced Analytics Dashboards
1. **Admin Analytics**: Application funnel bar chart, category doughnut chart, skill demand ranking, work type distribution, 6-month user/posting trends, AI match score histogram, and University Leaderboard.
2. **Student Analytics**: Personal application status breakdown, submission timeline, and weekly report score progress line chart.
3. **Company Analytics**: Recruitment funnel, monthly applicant trends, per-listing applicant counts, and top AI-ranked candidates.
4. **Supervisor Analytics**: Report status breakdown and student performance ranking bar chart.

### 3.4 Direct Messaging & Notifications
1. **Threaded Messaging**: Users can compose messages to any platform user. Automatically checks for existing threads or creates a new `Conversation`.
2. **Real-time Badges**: Global context processor calculates `unread_notifications_count` and `unread_messages_count` for live sidebar badges.

### 3.5 Recruitment ATS Pipeline & Academic Monitoring
1. **Pipeline Progression**: Recruiters advance applications through 7 status stages.
2. **Interview Scheduling**: Triggers notifications with meeting links (Google Meet/Zoom) or physical addresses.
3. **Weekly Reports & Evaluations**: Accepted students submit weekly reports. Assigned supervisors grade reports (0-100) and complete formal evaluations.
