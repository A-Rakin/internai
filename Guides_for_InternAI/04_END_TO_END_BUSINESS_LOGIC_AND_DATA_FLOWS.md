# 04. End-to-End Business Logic & Data Flows

---

## 🔄 1. Complete Workflow Diagrams & Data Traversal

### 1.1 Flow 1: AI Resume Parsing & Skill Match Scoring
When a student applies for an internship with a PDF resume:

```
[Student Uploads PDF Resume] ──> [submit_application view]
                                         │
                                         ▼
                      [common/ai_engine.py: extract_text_from_pdf()]
                                         │ (Parses plain text using pypdf)
                                         ▼
                      [common/ai_engine.py: calculate_skill_match()]
                                         │
             ┌───────────────────────────┴──────────────────────────┐
             ▼ (Groq Cloud API Key Active)                          ▼ (Offline Fallback)
    [Groq Cloud API (Llama 3.3 70B)]                     [_local_skill_match()]
    - Evaluates 4 dimensions:                           - Regex Keyword Matching
      1. Technical Skills (0-40)                        - Basic Match Calculation
      2. Project Experience (0-25)
      3. Education Alignment (0-15)
      4. CV Formatting (0-20)
             │                                                      │
             └───────────────────────────┬──────────────────────────┘
                                         ▼
                       [Calculated Total Match Score (0-98%)]
                                         │
                                         ▼
                       [Saved to Application.ai_match_score in DB]
                                         │
                                         ▼
                       [Displayed in Company ATS Candidate Rank]
```

---

### 1.2 Flow 2: Recruitment ATS Pipeline Status Transition
Recruiter advances candidate through 7 status stages:

```
[Pending] ──> [Reviewing] ──> [Assessment] ──> [Interview] ──> [Offer] ──> [Accepted] / [Rejected]
```
1. Company clicks status update button in ATS dashboard (`applications/views.py: update_status`).
2. `Application.status` field is updated in database.
3. Automatically triggers `Notification.objects.create()` to alert student in real-time.

---

### 1.3 Flow 3: AI Chatbot Request Flow
Floating chatbot interaction step-by-step:

1. User types prompt in Floating Widget input box and submits.
2. JavaScript sends AJAX `POST` request to `/chatbot/api/`.
3. `chatbot/views.py: chat_api()` receives request:
   - Fetches or creates active `ChatSession` for `request.user`.
   - Constructs a **Role-Aware System Prompt** (giving AI context on whether user is Student, Company, or Supervisor).
   - Sends full chat history + prompt to **Groq Cloud LLM API (`llama-3.3-70b-versatile`)**.
   - Receives AI answer, saves both User Message and Assistant Message to `ChatMessage` table in DB.
   - Returns JSON response `{"response": "AI text..."}` to frontend JavaScript.
4. JavaScript dynamically appends message bubble to chat window without refreshing the page.

---

### 1.4 Flow 4: Chart.js Analytics Data Generation
How visual charts get populated:

1. Student/Company/Admin visits dashboard (`/analytics/student/`).
2. `analytics/views.py` runs Django ORM aggregation queries:
   ```python
   # Example: Count applications per status
   status_counts = Application.objects.filter(student=user).values('status').annotate(count=Count('id'))
   ```
3. View serializes output into JSON arrays: `labels = ['Pending', 'Interview', 'Offer']`, `data = [5, 2, 1]`.
4. Renders template passing arrays in context dictionary.
5. In HTML template, Chart.js initializes HTML `<canvas id="appChart"></canvas>` element with context data.
