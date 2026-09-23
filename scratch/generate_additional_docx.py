import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

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
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
        
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run(title_text)
    run_title.font.name = 'Calibri'
    run_title.font.size = Pt(24)
    run_title.font.bold = True
    run_title.font.color.rgb = PRIMARY_COLOR
    p_title.paragraph_format.space_after = Pt(4)
    
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
# DOCUMENT 5: Button Execution Mechanics Guide
# ==============================================================================
def generate_button_doc():
    doc = create_styled_document(
        "InternAI - Button Execution Mechanics & Technical Action Flows",
        "Deep-Dive Architecture into How Buttons Perform in Django & Trace of Every Key Button in InternAI"
    )

    add_heading_1(doc, "1. How Buttons Function in Django Architecture")
    add_paragraph(doc, "In Django applications, user interaction is initiated via UI buttons. Buttons operate under three fundamental web execution paradigms:")

    add_heading_2(doc, "A. Anchor Link Buttons (HTTP GET Request)")
    add_paragraph(doc, "Rendered using HTML <a> tags styled as CSS buttons. Clicking sends an HTTP GET request to navigate between views or load data without mutating backend state.")
    add_code_block(doc, "<a href=\"{% url 'internships:detail' pk=internship.id %}\" class=\"btn btn-primary\">\n    View Details\n</a>")
    add_bullet(doc, "Browser triggers GET /internships/detail/5/", "Flow: ")
    add_bullet(doc, "urls.py matches path to view function internships.views.detail", "Routing: ")
    add_bullet(doc, "View queries database and renders HTML template.", "Response: ")

    add_heading_2(doc, "B. Form Submit Buttons (HTTP POST Request with CSRF Token)")
    add_paragraph(doc, "Rendered using <button type=\"submit\"> inside HTML forms. Used for state-changing database operations (Create, Update, Delete). Must include standard Django CSRF security tokens.")
    add_code_block(doc, "<form method=\"POST\" action=\"{% url 'applications:submit' internship.id %}\">\n    {% csrf_token %}\n    <button type=\"submit\" class=\"btn btn-success\">\n        Submit Application\n    </button>\n</form>")
    add_bullet(doc, "Sends form payload + CSRF token via POST request.", "Flow: ")
    add_bullet(doc, "CsrfViewMiddleware validates security token.", "Security: ")
    add_bullet(doc, "View function validates form data, saves record to database, adds user feedback message, and issues HTTP 302 Redirect.", "Execution: ")

    add_heading_2(doc, "C. Asynchronous AJAX / JavaScript Buttons")
    add_paragraph(doc, "Rendered using <button onclick=\"...\">. Uses JavaScript fetch() or XMLHttpRequest to communicate with Django JSON endpoints without reloading the webpage.")
    add_code_block(doc, "<button onclick=\"generateCoverLetter(12)\" class=\"btn btn-secondary\">\n    Generate AI Cover Letter\n</button>")
    add_bullet(doc, "JavaScript intercepts click, calls fetch('/applications/generate-cover-letter/12/').", "Flow: ")
    add_bullet(doc, "Django view processes request and returns JsonResponse({'cover_letter': '...'}).", "Backend: ")
    add_bullet(doc, "JavaScript updates DOM text dynamically.", "DOM Update: ")

    add_heading_1(doc, "2. Complete Trace of Major Buttons in InternAI")
    
    headers_btn = ["Button Name & UI Context", "HTTP Method & Tech Type", "Target URL & View Name", "Backend Database Action"]
    rows_btn = [
        ["Apply Now (Internship Detail)", "HTTP GET / POST", "applications:submit", "Creates new Application model instance linked to Student and Internship."],
        ["Post Internship (Company)", "HTTP POST", "companies:post_internship", "Validates InternshipForm and saves new Internship object with status='open'."],
        ["Quick Approve (Recruiter)", "HTTP POST", "companies:update_app_status", "Updates Application.status = 'accepted' and triggers notification."],
        ["Submit Weekly Report (Student)", "HTTP POST", "reports:create_report", "Saves WeeklyReport instance with logbook details for supervisor review."],
        ["Grade Logbook (Supervisor)", "HTTP POST", "supervisors:grade_report", "Updates WeeklyReport.score, status = 'approved', and adds feedback remarks."],
        ["Approve Job Post (Admin)", "HTTP POST", "administration:approve_post", "Sets Internship.is_approved = True and publishes position live."],
        ["Pay & Subscribe (Billing)", "HTTP POST", "billing:process_checkout", "Creates PaymentTransaction record, updates Subscription status to active."],
        ["Generate Cover Letter", "AJAX JSON POST", "applications:ai_cover_letter", "Executes AI text engine and returns JSON string to update modal."]
    ]
    add_table(doc, headers_btn, rows_btn)

    add_heading_1(doc, "3. Step-by-Step Code Execution Trace for 'Apply Now' Button")
    add_paragraph(doc, "To demonstrate complete technical mastery during defense, trace the 'Apply Now' button execution:")

    add_paragraph(doc, "Step 1: HTML Markup in Template (internships/detail.html)", bold_prefix="")
    add_code_block(doc, "<a href=\"{% url 'applications:submit' internship.id %}\" class=\"btn btn-primary btn-lg\">\n    Apply Now\n</a>")

    add_paragraph(doc, "Step 2: URL Pattern Resolution (applications/urls.py)", bold_prefix="")
    add_code_block(doc, "path('submit/<int:internship_id>/', views.submit_application, name='submit'),")

    add_paragraph(doc, "Step 3: View Function Execution (applications/views.py)", bold_prefix="")
    add_code_block(doc, "@login_required\n@role_required('student')\ndef submit_application(request, internship_id):\n    internship = get_object_or_404(Internship, pk=internship_id)\n    if request.method == 'POST':\n        form = ApplicationForm(request.POST, request.FILES)\n        if form.is_valid():\n            app = form.save(commit=False)\n            app.student = request.user.student_profile\n            app.internship = internship\n            app.save()\n            messages.success(request, 'Application submitted successfully!')\n            return redirect('students:applications')\n    return render(request, 'applications/submit.html', {'form': form})")

    add_callout(doc, "Always emphasize during defense: Buttons in Django do not execute Python code directly in HTML. Instead, buttons trigger HTTP requests that Django's URL Resolver maps to python view functions in views.py.", "BUTTON EXECUTION PRINCIPLE")

    filepath = os.path.join(OUTPUT_DIR, "button_execution_mechanics.docx")
    doc.save(filepath)
    print(f"Generated: {filepath}")

# ==============================================================================
# DOCUMENT 6: Payment System & Form Customization Guide
# ==============================================================================
def generate_payment_and_form_doc():
    doc = create_styled_document(
        "InternAI - Payment Architecture & Form Customization Master Guide",
        "In-Depth Payment Gateway Processing (bKash/Nagad/Cards) & Step-by-Step Tutorial for Adding/Deleting Form Fields"
    )

    add_heading_1(doc, "1. Payment Gateway & Subscription Architecture")
    add_paragraph(doc, "The billing system in InternAI handles monetized access for recruiting companies and premium student career plans. It integrates local Bangladeshi Mobile Financial Services (bKash, Nagad, Upay) as well as Credit/Debit card transactions.")

    add_heading_2(doc, "A. Core Database Schema for Billing")
    add_paragraph(doc, "The billing system is driven by two interrelated models defined in billing/models.py:")
    
    add_bullet(doc, "Tracks active and historical plans (e.g., Pro Recruiter Plan, Student Career Boost). Tracks amount, currency (BDT), started_at, expires_at, and automated 7-day expiration warning flags.", "1. Subscription Model: ")
    add_bullet(doc, "Records transaction receipts for audited payments. Fields include transaction_id (e.g., TXN-BKASH-894120), payment_method (bkash, nagad, upay, card), account_number, amount, and status (completed, pending, failed).", "2. PaymentTransaction Model: ")

    add_heading_2(doc, "B. Supported Payment Gateway Channels")
    headers_pay = ["Payment Channel", "Method Code", "Account Input Format", "Verification Process"]
    rows_pay = [
        ["bKash Mobile Banking", "bkash", "017XXXXXXXX (Mobile No)", "Instant PIN + OTP simulation & Transaction ID hash generation."],
        ["Nagad Mobile Banking", "nagad", "018XXXXXXXX (Mobile No)", "Automated payment verification callback."],
        ["Upay Mobile Banking", "upay", "019XXXXXXXX (Mobile No)", "Instant wallet balance transfer log."],
        ["Credit / Debit Card", "card", "Masked Card (**** 4242)", "Stripe/SSLCommerz sandbox token validation."]
    ]
    add_table(doc, headers_pay, rows_pay)

    add_heading_2(doc, "C. End-to-End Payment Transaction Flow")
    add_paragraph(doc, "When a company upgrades to a 'Pro Recruiter Plan' (BDT 5,000/month):")
    add_bullet(doc, "User selects plan tier on /billing/pricing/ and clicks 'Subscribe Now'.", "1. Plan Selection: ")
    add_bullet(doc, "User chooses payment method (bKash/Nagad/Card) and enters account details on /billing/checkout/.", "2. Checkout Submission: ")
    add_bullet(doc, "Django view processes payment form inside billing/views.py:", "3. Backend Processing: ")
    add_code_block(doc, "@login_required\ndef process_checkout(request):\n    if request.method == 'POST':\n        plan_name = request.POST.get('plan_name')\n        method = request.POST.get('payment_method')\n        amount = request.POST.get('amount')\n        \n        # 1. Create Payment Transaction Record\n        txn = PaymentTransaction.objects.create(\n            user=request.user,\n            transaction_id=f'TXN-{method.upper()}-{uuid.uuid4().hex[:8].upper()}',\n            payment_method=method,\n            amount=amount,\n            status='completed'\n        )\n        \n        # 2. Activate or Extend Subscription\n        sub, created = Subscription.objects.get_or_create(user=request.user)\n        sub.plan_name = plan_name\n        sub.expires_at = timezone.now() + timedelta(days=30)\n        sub.is_active = True\n        sub.save()\n        \n        messages.success(request, 'Payment successful! Subscription activated.')\n        return redirect('billing:receipt', txn_id=txn.transaction_id)")

    add_heading_1(doc, "2. Tutorial: How to Add or Delete Form Fields in Django")
    add_paragraph(doc, "During defense examinations, examiners frequently test students by asking: \"Add a new field (e.g. LinkedIn Profile URL or Expected Stipend) to this form\" or \"Remove a field\". Follow this exact 5-step blueprint:")

    add_heading_2(doc, "Blueprint: Adding a New Field ('linkedin_url') to Student Profile Form")

    add_paragraph(doc, "Step 1: Modify Database Model Schema (accounts/models.py)", bold_prefix="")
    add_paragraph(doc, "Open models.py and add the new field definition to the target class:")
    add_code_block(doc, "class StudentProfile(models.Model):\n    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)\n    university = models.CharField(max_length=150)\n    # NEW FIELD ADDED HERE:\n    linkedin_url = models.URLField('LinkedIn Profile', blank=True, null=True)")

    add_paragraph(doc, "Step 2: Generate & Apply Database Migrations (Terminal)", bold_prefix="")
    add_paragraph(doc, "Run migration commands in terminal to update SQL table structure:")
    add_code_block(doc, "python manage.py makemigrations accounts\npython manage.py migrate")

    add_paragraph(doc, "Step 3: Update Django Form Class (accounts/forms.py)", bold_prefix="")
    add_paragraph(doc, "Include the new field in Meta fields list and add widget styling:")
    add_code_block(doc, "class StudentProfileForm(forms.ModelForm):\n    class Meta:\n        model = StudentProfile\n        fields = ['university', 'major', 'gpa', 'linkedin_url'] # ADDED HERE\n        widgets = {\n            'linkedin_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/username'}),\n        }")

    add_paragraph(doc, "Step 4: Update HTML Form Template (students/templates/profile_edit.html)", bold_prefix="")
    add_paragraph(doc, "Add input rendering inside the template HTML:")
    add_code_block(doc, "<div class=\"mb-3\">\n    <label for=\"id_linkedin_url\" class=\"form-label\">LinkedIn Profile URL</label>\n    {{ form.linkedin_url }}\n</div>")

    add_paragraph(doc, "Step 5: Process Field Data in View Function (students/views.py)", bold_prefix="")
    add_paragraph(doc, "Django ModelForms automatically save form fields during form.save(). If using custom views, access data via form.cleaned_data['linkedin_url']:")
    add_code_block(doc, "if form.is_valid():\n    linkedin_url = form.cleaned_data.get('linkedin_url')\n    form.save()")

    add_heading_2(doc, "Blueprint: Deleting an Existing Field from a Form")
    add_bullet(doc, "Open forms.py and remove the target field string from fields = [...] list inside Meta class.", "1. Remove from Form Class: ")
    add_bullet(doc, "Open the HTML template and remove the corresponding <div> rendering {{ form.field_name }}.", "2. Remove from HTML Template: ")
    add_bullet(doc, "(Optional) If removing field permanently from database, delete field from models.py and run makemigrations + migrate.", "3. Database Cleanup: ")

    filepath = os.path.join(OUTPUT_DIR, "payment_system_and_form_customization.docx")
    doc.save(filepath)
    print(f"Generated: {filepath}")

if __name__ == "__main__":
    generate_button_doc()
    generate_payment_and_form_doc()
    print("ALL ADDITIONAL DOCX GUIDES GENERATED SUCCESSFULLY IN D:\\Guides for InternAI\\new")
