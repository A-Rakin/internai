# InternAI — AI-Powered Internship Management & Recruitment Platform

InternAI is a modern, enterprise-grade, AI-powered internship management and recruitment platform built using **Django**, **Bootstrap 5**, **Chart.js**, and **Vanilla CSS/JS**. It provides tailored portals for four distinct roles: **Students**, **Companies (HR Recruiters)**, **Academic Supervisors**, and **System Administrators**.

---

## 🌟 Key Platform Features

### 🤖 AI Ecosystem
- **AI-Powered Chatbot Assistant**: Embedded floating bot on every page + full-page chat interface powered by Groq Llama 3.3.
- **AI Resume Match Scoring**: Automatic PDF resume text extraction and skill compatibility calculation (0-100%).
- **AI Cover Letter Generator**: One-click generation of tailored cover letters based on student profiles and job requirements.
- **AI Interview Prep Coach**: Role-specific mock interview questions and real-time AI answer grading with feedback.

### 📊 Visual Analytics & Intelligence
- Interactive Chart.js dashboards for all roles.
- Application pipeline funnels, top skill demand charts, university leaderboards, monthly trends, and score distribution histograms.

### 💬 Internal Communication & Community
- **Direct Messaging System**: Real-time conversation threading between students, recruiters, and academic supervisors.
- **In-App Notifications**: Unread badges and instant alerts for application status updates, interview schedules, and messages.

### 💼 Recruitment & Academic Management
- **Applicant Tracking System (ATS)**: Multi-stage pipeline (`pending` → `reviewing` → `assessment` → `interview` → `offer` → `accepted`).
- **Interview Scheduling**: Supports online (Google Meet/Zoom), on-site, and phone interview formats.
- **Academic Monitoring**: Weekly student activity reports, supervisor grading (0-100), and formal performance evaluation forms.
- **Saved Internships (Bookmarks)**: One-click bookmarking of positions for students.
- **Stripe Subscriptions**: Tiered pricing (`pro` / `ultimate`) for companies with local fallback mode.

---

## 🚀 How to Run in Visual Studio Code (Windows)

### Step 1: Open Project Directory
```powershell
# Open VS Code in the project root
code E:\InternAi
```

### Step 2: Activate Virtual Environment
```powershell
.\venv\Scripts\activate
```

### Step 3: Run Database Migrations
```powershell
.\venv\Scripts\python.exe manage.py makemigrations
.\venv\Scripts\python.exe manage.py migrate
```

### Step 4: Create an Admin Account
```powershell
.\venv\Scripts\python.exe manage.py createsuperuser
```

### Step 5: Start the Server
```powershell
.\venv\Scripts\python.exe manage.py runserver
```

### Step 6: Open Web Browser
Navigate to 👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 📂 System Architecture & Modules

```
InternAi/
├── accounts/        # User auth, custom user, Student/Company/Supervisor profiles, password reset
├── students/        # Student portal, applications, interview prep coach, saved internships
├── companies/       # Recruiter portal, ATS pipeline, candidate ranking, AI resume analysis
├── supervisors/     # Academic supervision, student roster, weekly report review & evaluations
├── internships/     # Internship listings, categories, search/filter engine, saved internships
├── applications/    # Application submission, AI cover letter generator, pipeline tracking
├── interviews/      # Interview scheduling, modes, outcomes, meeting links
├── reports/         # Weekly report submission, grading, final evaluations
├── analytics/       # Visual analytics dashboard (Chart.js), funnel charts, skill demand, leaderboard
├── chatbot/         # AI Chatbot assistant (Groq Llama 3.3), floating widget, chat sessions
├── messaging/       # Internal direct messaging, conversation threading, unread counters
├── notifications/   # In-app notification delivery system
├── documents/       # File upload management, ActivityLog audit trail
├── administration/  # System administration, internship moderation, user management, activity logs
├── billing/         # Stripe payments & tier subscription checkout
└── common/          # AI engine (Groq LLM + local NLP fallback), landing pages, context processors
```

---

## 🔑 Environment Setup & API Keys

Create a `.env` file in the root directory:
```env
DEBUG=True
SECRET_KEY=your_django_secret_key
GROQ_API_KEY=gsk_your_groq_cloud_api_key
STRIPE_PUBLIC_KEY=your_stripe_public_key
STRIPE_SECRET_KEY=your_stripe_secret_key
```
*(Note: If no Groq API key is provided, the platform automatically uses intelligent local NLP fallbacks for all AI features).*
