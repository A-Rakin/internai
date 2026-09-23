import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

OUTPUT_DIR = r"D:\Guides for InternAI\new"
os.makedirs(OUTPUT_DIR, exist_ok=True)

PRIMARY_COLOR = RGBColor(26, 82, 118)     # #1A5276 (Deep Navy Blue)
SECONDARY_COLOR = RGBColor(40, 116, 166)  # #2874A6 (Slate Blue)
DARK_TEXT = RGBColor(44, 62, 80)          # #2C3E50 (Dark Charcoal)
CODE_COLOR = RGBColor(211, 84, 0)         # #D35400 (Orange/Rust)

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def create_styled_document(title_text, subtitle_text):
    doc = docx.Document()
    
    # Page setup - 1 inch margins
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
        
    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run(title_text)
    run_title.font.name = 'Calibri'
    run_title.font.size = Pt(24)
    run_title.font.bold = True
    run_title.font.color.rgb = PRIMARY_COLOR
    p_title.paragraph_format.space_after = Pt(4)
    
    # Subtitle
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = p_sub.add_run(subtitle_text)
    run_sub.font.name = 'Calibri'
    run_sub.font.size = Pt(13)
    run_sub.font.italic = True
    run_sub.font.color.rgb = SECONDARY_COLOR
    p_sub.paragraph_format.space_after = Pt(24)
    
    return doc

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = PRIMARY_COLOR

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = SECONDARY_COLOR

def add_paragraph(doc, text, bold_prefix="", italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Calibri'
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
        r_pre.font.color.rgb = DARK_TEXT
    r = p.add_run(text)
    r.font.name = 'Calibri'
    r.font.size = Pt(11)
    r.font.italic = italic
    r.font.color.rgb = DARK_TEXT

def add_bullet(doc, text, bold_prefix=""):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Calibri'
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
        r_pre.font.color.rgb = DARK_TEXT
    r = p.add_run(text)
    r.font.name = 'Calibri'
    r.font.size = Pt(11)
    r.font.color.rgb = DARK_TEXT

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F2F4F4")
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.left_indent = Inches(0.1)
    p.paragraph_format.right_indent = Inches(0.1)
    
    r = p.add_run(code_text)
    r.font.name = 'Consolas'
    r.font.size = Pt(9.5)
    r.font.color.rgb = CODE_COLOR
    
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def add_callout(doc, text, title="IMPORTANT DEFENSE TIP"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "EBF5FB")
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    
    r_title = p.add_run(f"📌 {title}: ")
    r_title.font.name = 'Calibri'
    r_title.font.size = Pt(10.5)
    r_title.font.bold = True
    r_title.font.color.rgb = PRIMARY_COLOR
    
    r_text = p.add_run(text)
    r_text.font.name = 'Calibri'
    r_text.font.size = Pt(10.5)
    r_text.font.italic = True
    r_text.font.color.rgb = DARK_TEXT
    
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def add_table(doc, headers, rows_data):
    tbl = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Header Row
    hdr_cells = tbl.rows[0].cells
    for i, header_text in enumerate(headers):
        hdr_cells[i].text = header_text
        set_cell_background(hdr_cells[i], "1A5276")
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in p.runs:
            run.font.name = 'Calibri'
            run.font.size = Pt(10)
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
            
    # Data Rows
    for row_idx, row_data in enumerate(rows_data):
        row_cells = tbl.rows[row_idx + 1].cells
        bg_color = "F9FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, cell_value in enumerate(row_data):
            row_cells[col_idx].text = cell_value
            set_cell_background(row_cells[col_idx], bg_color)
            p = row_cells[col_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.name = 'Calibri'
                run.font.size = Pt(9.5)
                run.font.color.rgb = DARK_TEXT
                
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

# ==============================================================================
# DOCUMENT 1: KPI Justification Guide
# ==============================================================================
def generate_kpi_doc():
    doc = create_styled_document(
        "InternAI - Key Performance Indicators (KPI) & Analytics Guide",
        "Comprehensive Justification, Formulas, Django Queries & Board Defense Strategy"
    )
    
    add_heading_1(doc, "1. Executive Summary: Role of KPIs in InternAI")
    add_paragraph(doc, "In modern web application engineering, Key Performance Indicators (KPIs) convert raw database records into high-level, actionable insights. In InternAI, KPIs drive data-informed decision making across four user roles: Platform Administrators, Students, Recruiting Companies, and Academic Supervisors.")
    
    add_bullet(doc, "Provides real-time visibility into overall platform growth, student placement conversion rates, skill trends, and institutional leaderboards.", "Administrator Role: ")
    add_bullet(doc, "Helps candidates evaluate their application success rate, monitor skill match alignment scores, and track weekly logbook evaluation scores.", "Student Role: ")
    add_bullet(doc, "Offers analytics on job post reach (views), candidate application velocity, hiring funnel progression, and top candidate match scores.", "Company (Recruiter) Role: ")
    add_bullet(doc, "Tracks supervisory workload, report review throughput, pending grading bottlenecks, and student performance metrics.", "Academic Supervisor Role: ")

    add_heading_1(doc, "2. Detailed KPI Metrics Breakdown by User Role")
    
    add_heading_2(doc, "A. Administrator KPIs")
    headers_admin = ["KPI Metric Name", "Calculation Logic / Formula", "Django ORM Query", "Business Value"]
    rows_admin = [
        ["Total Platform Users", "Count of all CustomUser records", "CustomUser.objects.count()", "Measures user growth and system adoption."],
        ["User Role Distribution", "Count of users grouped by role", "CustomUser.objects.filter(role=ROLE).count()", "Monitors balance between candidates and recruiters."],
        ["Active Open Vacancies", "Approved internships with status='open'", "Internship.objects.filter(status='open', is_approved=True).count()", "Tracks active placement opportunities."],
        ["Average AI Match Score", "Mean match score across applications", "Application.objects.filter(ai_match_score__isnull=False).aggregate(Avg('ai_match_score'))", "Evaluates algorithmic matching performance."],
        ["Application Funnel", "Volume breakdown by status stage", "Application.objects.filter(status=STATUS).count()", "Identifies conversion bottlenecks in hiring pipeline."],
        ["Top Skills Demand", "Frequency counter of required skills", "Counter(skills_list).most_common(10)", "Delivers market intelligence on in-demand technical skills."],
        ["University Leaderboard", "Accepted applications by university", "StudentProfile.objects.values('university').annotate(accepted=Count(...))", "Ranks institutional placement performance."]
    ]
    add_table(doc, headers_admin, rows_admin)

    add_heading_2(doc, "B. Student KPIs")
    headers_student = ["KPI Metric Name", "Formula / Logic", "Django ORM Implementation", "Student Practical Value"]
    rows_student = [
        ["Application Success Rate", "(Accepted Applications / Total Applied) * 100", "(Accepted / Total) * 100", "Measures application strategy effectiveness."],
        ["Average Match Score", "Mean match score of candidate applications", "applications.aggregate(avg=Avg('ai_match_score'))", "Indicates targeting accuracy for suitable jobs."],
        ["Weekly Report Score Trend", "Average score of weekly logbook submissions", "WeeklyReport.objects.filter(student=profile).aggregate(Avg('score'))", "Tracks ongoing academic performance during internship."],
        ["Interview Shortlist Rate", "Applications reaching interview stage", "applications.filter(status='interview').count()", "Measures resume screening success."]
    ]
    add_table(doc, headers_student, rows_student)

    add_heading_2(doc, "C. Company (Recruiter) KPIs")
    headers_company = ["KPI Metric Name", "Formula / Logic", "Django ORM Implementation", "Recruiter Value"]
    rows_company = [
        ["Post Reach (Total Views)", "Sum of view counts across company job listings", "sum(internships.values_list('views_count', flat=True))", "Measures employer brand reach and attraction."],
        ["Applicants per Listing", "Count of applications grouped by internship", "internships.annotate(app_count=Count('applications'))", "Evaluates job posting appeal."],
        ["Recruitment Funnel Velocity", "Count of applications in review, interview, offer", "applications.filter(status=STATUS).count()", "Monitors time-to-hire & candidate progression."],
        ["Top Candidate Match Index", "Candidates with AI match score >= 80%", "applications.order_by('-ai_match_score')[:10]", "Reduces resume screening overhead."]
    ]
    add_table(doc, headers_company, rows_company)

    add_heading_2(doc, "D. Academic Supervisor KPIs")
    headers_sup = ["KPI Metric Name", "Formula / Logic", "Django ORM Implementation", "Supervisor Value"]
    rows_sup = [
        ["Assigned Student Load", "Distinct students linked via logbooks", "reports.values_list('student_id', flat=True).distinct().count()", "Tracks supervisory responsibility."],
        ["Pending Review Throughput", "Reports submitted awaiting review", "reports.filter(status='submitted').count()", "Highlights grading bottlenecks."],
        ["Average Report Score", "Mean score of approved logbooks", "reports.aggregate(avg=Avg('score'))", "Assesses overall student work quality."]
    ]
    add_table(doc, headers_sup, rows_sup)

    add_heading_1(doc, "3. Django ORM Query Mechanics: Aggregate vs Annotate")
    add_paragraph(doc, "Understanding the distinction between aggregate() and annotate() is vital during defense examination:")
    add_bullet(doc, "Computes a single summary value across the entire QuerySet. Returns a Python dictionary. Example: Calculating platform-wide average match score.", "aggregate(): ")
    add_code_block(doc, "avg_score = Application.objects.aggregate(avg=Avg('ai_match_score'))['avg']")
    add_bullet(doc, "Computes summary values for each row in a QuerySet (equivalent to SQL GROUP BY). Returns an annotated QuerySet. Example: Counting applications per internship listing.", "annotate(): ")
    add_code_block(doc, "listings = Internship.objects.annotate(app_count=Count('applications')).order_by('-app_count')")

    add_heading_1(doc, "4. Defense Board Q&A Script for KPIs")
    add_paragraph(doc, "Q: Why did you implement a KPI dashboard instead of simple tabular reports?", bold_prefix="")
    add_paragraph(doc, "Answer: Basic tables display static data, whereas KPIs transform raw data into actionable decision support. For example, the Application Funnel KPI instantly highlights recruitment bottlenecks, while the AI Match Score KPI evaluates candidate fit efficiency.", italic=True)
    
    add_callout(doc, "When asked about Chart.js integration, explain that Django serializes ORM aggregations into JSON strings using json.dumps(), which are then passed into template context and rendered into HTML5 canvas charts via Chart.js scripts.", "CHART RENDERING TIP")

    filepath = os.path.join(OUTPUT_DIR, "kpi_justification.docx")
    doc.save(filepath)
    print(f"Generated: {filepath}")

# ==============================================================================
# DOCUMENT 2: Theoretical Knowledge Guide
# ==============================================================================
def generate_theory_doc():
    doc = create_styled_document(
        "InternAI - Comprehensive Django & Web Engineering Theoretical Guide",
        "Mastering Architecture, Lifecycle, ORM Internals, Commands & Security for Board Defense"
    )

    add_heading_1(doc, "1. Architectural Blueprint: Django MVT Pattern")
    add_paragraph(doc, "Django implements the MVT (Model-View-Template) architectural pattern. Unlike standard MVC (Model-View-Controller), Django itself acts as the Controller, leaving developers to focus on Models, Views, and Templates.")
    add_bullet(doc, "Defines data structure, ORM fields, relationships, and business logic validation rules.", "Model (models.py): ")
    add_bullet(doc, "Contains execution logic. Processes HTTP requests, queries Models, and renders HTML Templates or returns HTTP/JSON responses.", "View (views.py): ")
    add_bullet(doc, "Presentation layer. Renders HTML using Django Template Language (DTL) tags ({% %}) and context variables ({{ }}).", "Template (templates/): ")

    add_heading_1(doc, "2. Complete Web Request-Response Lifecycle in Django")
    add_paragraph(doc, "When a client submits a request to InternAI (e.g., navigating to /internships/):")
    add_bullet(doc, "The HTTP request hits WSGI (gunicorn/runserver) or ASGI (uvicorn/daphne).", "1. Web Server Entry: ")
    add_bullet(doc, "Django loads settings.py configuration (INSTALLED_APPS, DATABASES, MIDDLEWARE).", "2. System Settings: ")
    add_bullet(doc, "Request executes sequentially through Security, Session, Authentication, and CSRF middlewares.", "3. Request Middlewares: ")
    add_bullet(doc, "Django URL Resolver matches request path against root urls.py and app-level urls.py using regex/path converters.", "4. URL Dispatcher: ")
    add_bullet(doc, "View function/class executes business logic, enforcing @login_required decorators and executing ORM queries.", "5. View Execution: ")
    add_bullet(doc, "Django Template Engine compiles HTML templates with context dictionaries.", "6. Template Rendering: ")
    add_bullet(doc, "Response travels back through response middlewares and returns an HTTP status code (200 OK, 302 Redirect).", "7. HTTP Response: ")

    add_heading_1(doc, "3. Django App Directory Structure & File Roles")
    headers_files = ["File Name", "Core Purpose in Django Architecture", "InternAI Practical Example"]
    rows_files = [
        ["__init__.py", "Marks directory as a Python importable package.", "Enables Python module imports across apps."],
        ["apps.py", "App configuration and metadata class.", "Defines ApplicationsConfig and default auto field."],
        ["models.py", "Database tables defined as Python classes.", "Defines CustomUser, Internship, Application, WeeklyReport."],
        ["views.py", "Business logic handling HTTP requests.", "Renders analytics dashboard, candidate application handlers."],
        ["urls.py", "Maps endpoint paths to view functions.", "path('submit/<int:pk>/', views.submit_application, name='submit')"],
        ["admin.py", "Registers models with Django Admin Portal.", "admin.site.register(Internship, InternshipAdmin)"],
        ["signals.py", "Decoupled event listeners.", "Automatically creates StudentProfile when a CustomUser is registered."],
        ["migrations/", "Tracks schema changes to compile into SQL DDL.", "Contains python migration files generated by makemigrations."]
    ]
    add_table(doc, headers_files, rows_files)

    add_heading_1(doc, "4. Advanced Django ORM Concepts & Optimizations")
    add_heading_2(doc, "A. Field Lookups & Filtering")
    add_code_block(doc, "# Exact match and field lookups (__icontains, __gte)\nopen_jobs = Internship.objects.filter(status='open', is_approved=True)\nsearch_jobs = Internship.objects.filter(title__icontains='Python')\nhigh_match = Application.objects.filter(ai_match_score__gte=80)")

    add_heading_2(doc, "B. Q Objects and F Expressions")
    add_paragraph(doc, "Q objects enable complex SQL AND/OR queries. F expressions enable database-level field operations without loading data into Python memory.")
    add_code_block(doc, "from django.db.models import Q, F\n\n# OR query using Q\nremote_or_dhaka = Internship.objects.filter(Q(location='Remote') | Q(location='Dhaka'))\n\n# F expression: Atomic counter increment\nInternship.objects.filter(id=5).update(views_count=F('views_count') + 1)")

    add_heading_2(doc, "C. Query Optimization: select_related vs prefetch_related")
    add_bullet(doc, "Executes an SQL JOIN query. Used for Single-Value Relationships (ForeignKey and OneToOne). Eliminates N+1 query problems.", "select_related(*fields): ")
    add_code_block(doc, "apps = Application.objects.select_related('student__user', 'internship').all()")
    add_bullet(doc, "Executes separate SQL queries and performs joins in Python memory. Used for Multi-Value Relationships (ManyToManyField and reverse ForeignKeys).", "prefetch_related(*lookups): ")
    add_code_block(doc, "categories = InternshipCategory.objects.prefetch_related('internships').all()")

    add_heading_1(doc, "5. Core Management Commands")
    headers_cmd = ["Command", "Execution Action & Purpose"]
    rows_cmd = [
        ["python manage.py runserver", "Launches local HTTP development web server at http://127.0.0.1:8000/"],
        ["python manage.py makemigrations", "Inspects models.py for edits and generates migration scripts in migrations/"],
        ["python manage.py migrate", "Applies pending migration scripts to update database schema tables."],
        ["python manage.py createsuperuser", "Interactively creates an administrative root account."],
        ["python manage.py collectstatic", "Gathers static assets (CSS/JS) into STATIC_ROOT for production deployment."],
        ["python manage.py shell", "Opens an interactive Python shell pre-configured with Django environment."]
    ]
    add_table(doc, headers_cmd, rows_cmd)

    add_heading_1(doc, "6. Security & Authentication Architecture")
    add_bullet(doc, "CustomUser model inherits from AbstractUser with role choices ('student', 'company', 'supervisor', 'admin').", "Custom User Model: ")
    add_bullet(doc, "Enforced via @login_required, @role_required('student'), and view-level role checks.", "Role-Based Access Control (RBAC): ")
    add_bullet(doc, "CSRF tokens generated via {% csrf_token %}, SQL injection blocked by ORM query parameterization, XSS blocked by template auto-escaping.", "Security Mechanisms: ")

    filepath = os.path.join(OUTPUT_DIR, "theoretical_knowledge.docx")
    doc.save(filepath)
    print(f"Generated: {filepath}")

# ==============================================================================
# DOCUMENT 3: Project Demonstration Guide
# ==============================================================================
def generate_demo_doc():
    doc = create_styled_document(
        "InternAI - Practical Board Demonstration & Defense Script",
        "Step-by-Step Presentation Script, Pre-Demo Checklist & Live Feature Demonstration Sequence"
    )

    add_heading_1(doc, "1. Pre-Demonstration Room Setup Checklist")
    add_paragraph(doc, "Before calling examiners to view your presentation monitor, execute the following setup sequence:")
    add_bullet(doc, "Navigate to d:\\InternAi\\InternAi and activate virtual environment.", "1. Terminal Setup: ")
    add_code_block(doc, "cd d:\\InternAi\\InternAi\nvenv\\Scripts\\activate\npython manage.py runserver")
    add_bullet(doc, "Open browser and pre-load key endpoints in separate tabs:", "2. Browser Tabs Setup: ")
    add_bullet(doc, "http://127.0.0.1:8000/ (Landing Page)")
    add_bullet(doc, "http://127.0.0.1:8000/analytics/dashboard/ (Analytics & KPIs)")
    add_bullet(doc, "http://127.0.0.1:8000/administration/moderation/ (Admin Panel)")
    add_bullet(doc, "http://127.0.0.1:8000/admin/ (Django Native Admin)")
    add_bullet(doc, "Keep credentials sheet ready: Admin (admin / password123), Student (student1 / password123), Company (company1 / password123), Supervisor (supervisor1 / password123).", "3. Test Credentials: ")

    add_heading_1(doc, "2. 90-Second Opening Elevator Pitch")
    add_callout(doc, "\"Honorable Board Members, our project is InternAI — an end-to-end Smart Internship Management & AI-Powered Candidate Matching Portal. Traditional internship portals suffer from manual resume screening, lack of academic supervision, and static job lists. InternAI unifies four core stakeholders: Students (applications, AI match scores, weekly logbooks), Companies (job posts, applicant funnels, AI candidate screening), Academic Supervisors (student monitoring, logbook grading), and Administrators (platform moderation & analytics).\"", "VERBATIM OPENING SCRIPT")

    add_heading_1(doc, "3. Step-by-Step Live Feature Demonstration Sequence")
    
    add_heading_2(doc, "Step 1: Public Landing Page & Search (http://127.0.0.1:8000/)")
    add_paragraph(doc, "Show clean responsive UI, live system metrics counters (Total Internships, Companies, Hired Students), and the search bar.")

    add_heading_2(doc, "Step 2: Admin Moderation & Analytics Dashboard")
    add_paragraph(doc, "Log in as Admin (admin). Open /analytics/dashboard/ and highlight Chart.js visualizations:")
    add_bullet(doc, "Point out stage conversion drop-offs.", "Application Funnel: ")
    add_bullet(doc, "Show dynamic skill extraction from postings.", "Top Skills Demand: ")
    add_bullet(doc, "Highlight student placement counts by university.", "University Leaderboard: ")
    add_paragraph(doc, "Open /administration/moderation/ to demonstrate internship approvals and user verification controls.")

    add_heading_2(doc, "Step 3: Recruiter / Company Journey")
    add_paragraph(doc, "Log in as Company (company1). Navigate to Company Dashboard:")
    add_bullet(doc, "Show posted internship positions and applicant lists.", "Job Postings: ")
    add_bullet(doc, "Point out algorithmic match suitability percentage (e.g., 88% Match).", "AI Match Score: ")
    add_bullet(doc, "Demonstrate changing candidate status from Pending -> Interview -> Offer.", "Status Progression: ")

    add_heading_2(doc, "Step 4: Student Application & Logbook Journey")
    add_paragraph(doc, "Log in as Student (student1). Navigate to /internships/:")
    add_bullet(doc, "Submit application with resume attachment and cover note.", "Application Submission: ")
    add_bullet(doc, "Navigate to /reports/ and demonstrate filing a Weekly Logbook entry (tasks completed, learnings, challenges).", "Weekly Logbook Report: ")

    add_heading_2(doc, "Step 5: Academic Supervisor Oversight")
    add_paragraph(doc, "Log in as Supervisor (supervisor1). Navigate to Supervisor Dashboard:")
    add_bullet(doc, "View list of assigned interning students.", "Assigned Students: ")
    add_bullet(doc, "Open a submitted weekly report, assign a score (e.g., 90/100), and add supervisor remarks.", "Report Grading: ")

    add_heading_1(doc, "4. Defense Board Q&A Tactics")
    add_paragraph(doc, "Q: How does the AI Match Score work in your codebase?", bold_prefix="")
    add_paragraph(doc, "Answer: The AI Match Score calculates candidate skill match against internship requirement tags, weighted by profile completeness, location preference, and GPA. The float score is saved on the Application model for instant aggregation.", italic=True)

    filepath = os.path.join(OUTPUT_DIR, "project_demonstration_guide.docx")
    doc.save(filepath)
    print(f"Generated: {filepath}")

# ==============================================================================
# DOCUMENT 4: Shortcut Techniques Guide
# ==============================================================================
def generate_shortcut_doc():
    doc = create_styled_document(
        "InternAI - Live Code Modification & Defense Shortcuts Cheatsheet",
        "10-Second Page Finder Formula, Live UI Edits, Button Additions & Emergency Hacks"
    )

    add_heading_1(doc, "1. The 10-Second Page Finder Formula")
    add_paragraph(doc, "When examiners point to a web page and ask: \"Where is this rendered in code?\", follow this 3-step tracing formula:")
    add_callout(doc, "Browser URL endpoint  ===>  Lookup in urls.py  ===>  Opens views.py function  ===>  Renders template.html", "PAGE FINDER FORMULA")
    
    add_paragraph(doc, "Example Execution:")
    add_bullet(doc, "Browser URL is http://127.0.0.1:8000/applications/", "1. Endpoint: ")
    add_bullet(doc, "Open applications/urls.py -> search for path('', views.application_list, name='list').", "2. URL Route: ")
    add_bullet(doc, "Open applications/views.py -> locate def application_list(request):.", "3. View Logic: ")
    add_bullet(doc, "Check render(request, 'applications/application_list.html', context) at end of function.", "4. Template: ")
    add_bullet(doc, "Open applications/templates/applications/application_list.html.", "5. HTML File: ")

    add_heading_1(doc, "2. Recipe 1: Changing Button Colors & Styles Live")
    add_paragraph(doc, "Examiner Request: \"Change this button color to green or yellow right now.\"")
    add_bullet(doc, "Locate HTML template using 10-Second Page Finder Formula.", "Step 1: ")
    add_bullet(doc, "Press Ctrl+F in VS Code and search for button label text (e.g., 'Apply Now').", "Step 2: ")
    add_bullet(doc, "Replace CSS button class or add inline style attribute:", "Step 3: ")
    add_code_block(doc, "<!-- ORIGINAL -->\n<a href=\"#\" class=\"btn btn-primary\">Apply Now</a>\n\n<!-- CHANGED TO GREEN (Bootstrap) -->\n<a href=\"#\" class=\"btn btn-success\">Apply Now</a>\n\n<!-- GUARANTEED CUSTOM INLINE STYLE -->\n<a href=\"#\" class=\"btn\" style=\"background-color: #28a745; color: white;\">Apply Now</a>")
    add_bullet(doc, "Save file (Ctrl+S) and perform hard browser refresh (Ctrl+F5).", "Step 4: ")

    add_heading_1(doc, "3. Recipe 2: Adding a New Button with Live Functionality")
    add_paragraph(doc, "Examiner Request: \"Add a Quick Approve button on this page that changes status to accepted.\"")
    
    add_paragraph(doc, "1. Add HTML Button in Template (templates/.../detail.html):", bold_prefix="")
    add_code_block(doc, "<a href=\"{% url 'applications:quick_approve' app.id %}\" class=\"btn btn-success btn-sm\">\n    Quick Approve\n</a>")

    add_paragraph(doc, "2. Add URL Route in applications/urls.py:", bold_prefix="")
    add_code_block(doc, "path('quick-approve/<int:pk>/', views.quick_approve, name='quick_approve'),")

    add_paragraph(doc, "3. Add View Handler in applications/views.py:", bold_prefix="")
    add_code_block(doc, "@login_required\ndef quick_approve(request, pk):\n    app = get_object_or_404(Application, pk=pk)\n    app.status = 'accepted'\n    app.save()\n    messages.success(request, 'Application approved!')\n    return redirect('applications:detail', pk=pk)")

    add_heading_1(doc, "4. Recipe 3: Live Table & Data Column Addition")
    add_paragraph(doc, "Examiner Request: \"Add an AI Match Score column to this student table.\"")
    add_bullet(doc, "Add <th>AI Match Score</th> inside <thead> of table.", "1. Header: ")
    add_bullet(doc, "Add <td><span class=\"badge bg-info\">{{ app.ai_match_score }}%</span></td> inside <tbody> loop.", "2. Data Cell: ")

    add_heading_1(doc, "5. Recipe 4: Real-time DB Inspection via Django Shell")
    add_paragraph(doc, "In VS Code Terminal, launch interactive shell:")
    add_code_block(doc, "python manage.py shell\n\nfrom applications.models import Application\nfrom accounts.models import CustomUser\n\nprint('Total Users:', CustomUser.objects.count())\nfor app in Application.objects.all()[:3]:\n    print(app.student.user.username, app.status, app.ai_match_score)")

    add_heading_1(doc, "6. Emergency Troubleshooting Cheatsheet")
    headers_err = ["Symptom / Error", "Root Cause", "Instant Fix Solution"]
    rows_err = [
        ["Page didn't update", "Browser cached old static assets.", "Press Ctrl+Shift+R or Ctrl+F5."],
        ["NoReverseMatch Error", "Invalid URL pattern name in template.", "Verify path name parameter in urls.py."],
        ["TemplateDoesNotExist", "Incorrect template path in render().", "Check path relative to app's templates/ folder."],
        ["Server Hangs / Crashes", "Process locked or unhandled exception.", "Press Ctrl+C in terminal and run python manage.py runserver."]
    ]
    add_table(doc, headers_err, rows_err)

    filepath = os.path.join(OUTPUT_DIR, "shortcut_techniques.docx")
    doc.save(filepath)
    print(f"Generated: {filepath}")

if __name__ == "__main__":
    generate_kpi_doc()
    generate_theory_doc()
    generate_demo_doc()
    generate_shortcut_doc()
    print("ALL 4 DOCX GUIDES GENERATED SUCCESSFULLY IN D:\\Guides for InternAI\\new")
