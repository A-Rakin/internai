# InternAI — Final Defense Preparation & Codebase Mastery Kit

> **Location:** `D:\Guides for InternAI\`  
> **Prepared for:** Practicum Final Defense & Viva Board  
> **Project:** InternAI — AI-Powered Internship Management & Recruitment Platform  
> **Backend Framework:** Django 5 (Python 3.12) | **Database:** MySQL / SQLite3 | **Frontend:** HTML5, Bootstrap 5.3, Vanilla JS, CSS3, Chart.js  

---

## 📚 Overview of Defense Guides Included

This folder contains a complete, step-by-step master kit designed to give you **100% confidence** during your practical final defense board examination. 

Even if you have not written every line of code yourself, these documents break down every model, view, URL route, database relationship, AI engine, and template logic in clear, easy-to-understand **Bengali and English**.

---

## 📑 File Navigation & Study Roadmap

### 1. [`01_DEFENSE_OVERVIEW_AND_CHEATSHEET.md`](file:///D:/Guides%20for%20InternAI/01_DEFENSE_OVERVIEW_AND_CHEATSHEET.md)
- **What it covers:** 5-minute defense pitch script (Bengali & English), core Django MVT concepts, WSGI/ASGI, `@login_required` decorators, Request-Response life cycle, `.env` security, ORM vs Raw SQL.
- **When to read:** Start here first to get high-level clarity and learn how to speak confidently to the defense board.

### 2. [`02_PROJECT_STRUCTURE_AND_APP_DIRECTORY.md`](file:///D:/Guides%20for%20InternAI/02_PROJECT_STRUCTURE_AND_APP_DIRECTORY.md)
- **What it covers:** Complete directory map, breakdown of all 16 Django apps (`accounts`, `internships`, `applications`, `interviews`, `reports`, `analytics`, `chatbot`, `messaging`, `notifications`, `billing`, `documents`, `administration`, etc.).
- **When to read:** Read to understand where every file is located and what each function in `views.py` does.

### 3. [`03_DATABASE_SCHEMA_MODELS_AND_CONSTRAINTS.md`](file:///D:/Guides%20for%20InternAI/03_DATABASE_SCHEMA_MODELS_AND_CONSTRAINTS.md)
- **What it covers:** All 16 database models, fields, types, foreign key relationships (`1:1`, `1:N`, `M:N`), cascade deletions, indexing, constraints (`unique_together`, `validators`), and ER diagram structure.
- **When to read:** Read if examiners ask database schema questions or ask you to explain SQL relationships.

### 4. [`04_END_TO_END_BUSINESS_LOGIC_AND_DATA_FLOWS.md`](file:///D:/Guides%20for%20InternAI/04_END_TO_END_BUSINESS_LOGIC_AND_DATA_FLOWS.md)
- **What it covers:** Step-by-step trace of key platform features: User signup/login, Posting internships, AI resume PDF parsing & Groq Llama match scoring, Application ATS pipeline, Weekly reports, Floating AI Chatbot, Chart.js analytics.
- **When to read:** Read to explain exact data flow from browser submit button -> Django view -> ORM -> Database -> AI API -> Response.

### 5. [`05_LIVE_DEFENSE_CODE_MODIFICATION_GUIDE.md`](file:///D:/Guides%20for%20InternAI/05_LIVE_DEFENSE_CODE_MODIFICATION_GUIDE.md)
- **What it covers:** On-the-spot live editing cheat-sheet! How to change primary theme colors, change button styles, add database fields with `makemigrations`/`migrate`, edit business logic rules (GPA limits, user access rules), tweak template text and URLs.
- **When to read:** Keep open during your practical defense in case the board asks you to modify code live.

### 6. [`06_DEFENSE_QUESTIONS_AND_ANSWERS_BANK.md`](file:///D:/Guides%20for%20InternAI/06_DEFENSE_QUESTIONS_AND_ANSWERS_BANK.md)
- **What it covers:** Top 35+ expected viva questions (Django, Database, Security, AI, Frontend, Testing) with model Bengali/English answers.
- **When to read:** Practice answering these questions out loud before going into the defense room.

### 7. [`07_PRACTICUM_BOARD_QUESTIONS_AND_ANSWERS.md`](file:///D:/Guides%20for%20InternAI/07_PRACTICUM_BOARD_QUESTIONS_AND_ANSWERS.md)
- **What it covers:** Detailed Bengali & English model answers for actual practicum defense board questions (Project Problem Statement, Feature Selection Rationale, Input Validation & Live Code Edits, Dynamic URL Routing, Button & AJAX Performance, Form Field Addition/Deletion, PDF Export & Ascending/Descending Sorting, and Payment Gateway Workflow).
- **When to read:** Essential reading right before the defense board to confidently answer board-specific questions.

---

## ⚡ Quick Emergency Cheat-Sheet for Defense Room

| Task / Question | Where to look in Codebase | How to do it / Explain it |
| :--- | :--- | :--- |
| **Change Frontend Color Theme** | `static/css/style.css` or template CSS | Edit `--primary-color: #4f46e5;` CSS variable |
| **Change Login Redirection** | `accounts/views.py` (`login_view`) | Look at `role` conditional (`if user.role == 'student': redirect(...)`) |
| **What is `@login_required`?** | `common/decorators.py` or Django Auth | Python decorator checking `request.user.is_authenticated`. Redirects to login if False. |
| **Where is AI Resume Parsing?** | `common/ai_engine.py` | `extract_text_from_pdf()` uses `pypdf`, `calculate_skill_match()` calls Groq Cloud API |
| **Where is Chatbot Groq integration?** | `chatbot/views.py` (`chat_api`) | Collects session history, sends system prompt to Groq Llama 3.3 70B, returns JSON response |
| **Add field to Database** | `models.py` in target app | Add field, run `python manage.py makemigrations`, `python manage.py migrate` |
| **Run local server** | PowerShell / Terminal | `python manage.py runserver` |

---
*Good luck with your Defense! You are fully equipped to excel.*
