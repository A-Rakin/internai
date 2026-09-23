# InternAI - Shortcut Techniques & Live Code Modification Cheatsheet

During a practical board exam or defense, examiners often ask live modification questions such as:
- *"Where is this page located in code?"*
- *"Change this button color to green right now."*
- *"Add a new button here that triggers a new function."*
- *"Show me how data flows from database to this button."*

This cheat sheet provides 10-second shortcuts and step-by-step recipes to perform live modifications effortlessly.

---

## 1. The 10-Second Page Finder Rule (URL -> View -> Template)

Whenever an examiner points to a browser page and asks where it lives in the codebase, follow this 3-step formula:

```
[ Browser URL ]  ===>  Look in [ urls.py ]  ===>  Opens [ views.py ]  ===>  Renders [ template.html ]
```

### Formula Example:
1. **Browser URL**: `http://127.0.0.1:8000/applications/`
2. **Find URL Route**: Open `applications/urls.py` -> search for `path('', views.application_list, name='list')`.
3. **Find View Logic**: Open `applications/views.py` -> look for `def application_list(request):`.
4. **Find HTML Template**: At the bottom of `application_list`, look at `render(request, 'applications/application_list.html', context)`.
5. **Open HTML File**: `applications/templates/applications/application_list.html`.

---

## 2. Recipe 1: Changing Button Color & Text Live

Examiner request: *"Make this button blue/green/purple or change its text."*

### Steps:
1. Locate the HTML template file using **10-Second Page Finder**.
2. Press `Ctrl + F` inside VS Code and search for the button text (e.g., "Apply Now" or "Submit").
3. Update the CSS class or inline style:

```html
<!-- BEFORE (Default Primary Button) -->
<a href="#" class="btn btn-primary">Apply Now</a>

<!-- AFTER CHANGE 1: Using built-in Bootstrap / Theme classes -->
<a href="#" class="btn btn-success">Apply Now</a> <!-- Green -->
<a href="#" class="btn btn-warning">Apply Now</a> <!-- Yellow -->
<a href="#" class="btn btn-info">Apply Now</a>    <!-- Cyan/Blue -->

<!-- AFTER CHANGE 2: Custom Inline CSS Style (Guaranteed visual update) -->
<a href="#" class="btn" style="background-color: #28a745; color: #ffffff; padding: 10px 20px; border-radius: 5px;">
   Apply Now
</a>
```
4. Save file (`Ctrl + S`), go to browser, press `Ctrl + F5` (Hard Refresh).

---

## 3. Recipe 2: Adding a New Button with Live Functionality

Examiner request: *"Add a 'Quick Approve' button on this page that changes status or shows a message."*

### Step 1: Add HTML Button in Template (`templates/.../xyz.html`)
```html
<!-- Add near existing action buttons -->
<a href="{% url 'applications:quick_approve' app.id %}" class="btn btn-success btn-sm">
    <i class="bi bi-check-circle"></i> Quick Approve
</a>
```

### Step 2: Add URL Route in `applications/urls.py`
```python
path('quick-approve/<int:pk>/', views.quick_approve, name='quick_approve'),
```

### Step 3: Add View Function in `applications/views.py`
```python
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

@login_required
def quick_approve(request, pk):
    application = get_object_or_404(Application, pk=pk)
    application.status = 'accepted'
    application.save()
    messages.success(request, f"Application for {application.student.user.get_full_name()} approved successfully!")
    return redirect('applications:detail', pk=pk)
```
4. Save all files, refresh browser, click the new button to demonstrate live execution!

---

## 4. Recipe 3: Modifying Table Data / Display Fields Live

Examiner request: *"Add a column showing candidate Email or AI Match Score in this table."*

### Steps:
1. Open template file (e.g., `applications/templates/applications/application_list.html`).
2. Locate `<thead>` table header and add `<th>`:
   ```html
   <th>AI Match Score</th>
   ```
3. Locate `<tbody>` table row loop `{% for app in applications %}` and add `<td>`:
   ```html
   <td>
       <span class="badge bg-info">{{ app.ai_match_score|default:"N/A" }}%</span>
   </td>
   ```
4. Refresh browser!

---

## 5. Recipe 4: Quick Database Inspection via Django Shell

Examiner request: *"Show me the database records directly without opening DB Browser."*

### Steps:
1. In VS Code Terminal, run:
   ```bash
   python manage.py shell
   ```
2. Run these commands line by line:
   ```python
   from applications.models import Application
   from accounts.models import CustomUser

   # View total counts
   print("Total users:", CustomUser.objects.count())

   # View top 3 applications
   for app in Application.objects.all()[:3]:
       print(f"Student: {app.student.user.username}, Status: {app.status}, Score: {app.ai_match_score}")
   ```
3. Exit shell: `exit()`

---

## 6. Emergency Troubleshooting Cheatsheet

| Issue During Live Demo | Solution |
| :--- | :--- |
| **Page didn't update after template edit** | Press `Ctrl + Shift + R` or `Ctrl + F5` in browser to bypass cache. |
| **`NoReverseMatch` Template Error** | You used `{% url 'app_name:view_name' %}` but URL pattern name in `urls.py` is missing or misspelled. Check `urls.py`. |
| **`TemplateDoesNotExist` Error** | Check template path inside `render(request, 'path/file.html')`. Path is relative to app `templates/` folder. |
| **`IntegrityError` or Foreign Key Error** | Trying to create/save an object without assigning required ForeignKeys (e.g., student or company profile). |
| **Server Crashed / Terminal Stuck** | Press `Ctrl + C` in terminal and restart server: `python manage.py runserver`. |
