# 05. Live Defense Code Modification Handbook

---

## 🛠️ On-the-Spot Code Edits Cheat-Sheet

During your practical defense, examiners often ask you to perform quick live code modifications to verify that you understand the system architecture. Below are step-by-step instructions for the most common requested edits.

---

### 🎨 Scenario 1: Change Frontend Theme Colors & Styling

**Examiner Question:** *"Can you change the primary theme color of the platform from Blue/Indigo to Green or Dark Teal?"*

**Step-by-Step Fix:**
1. Open `static/css/style.css` (or `templates/base.html` `<style>` section).
2. Locate the CSS Root Variables at the top of the file:
   ```css
   :root {
       --primary-color: #4f46e5;      /* Original Indigo/Blue */
       --primary-hover: #4338ca;
   }
   ```
3. Change to new color hex code (e.g. Green `#10b981` or Teal `#0d9488`):
   ```css
   :root {
       --primary-color: #10b981;      /* New Emerald Green */
       --primary-hover: #059669;
   }
   ```
4. Save file and refresh browser page (`Ctrl + F5`). The navbar buttons, primary badges, and links will instantly change color!

---

### 🗃️ Scenario 2: Add a New Field to a Database Model

**Examiner Question:** *"Add a `stipend_type` field (Fixed vs Performance-Based) to the `Internship` model and display it on the internship detail page."*

**Step-by-Step Fix:**
1. Open `internships/models.py`.
2. Find class `Internship` and add the new field:
   ```python
   class Internship(models.Model):
       # ... existing fields ...
       stipend_type = models.CharField(
           max_length=50,
           choices=[('fixed', 'Fixed Monthly'), ('performance', 'Performance Based')],
           default='fixed'
       )
   ```
3. Save file and open PowerShell / Terminal in project directory.
4. Run migration commands:
   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Display the field in template `internships/templates/internships/internship_detail.html`:
   ```html
   <p><strong>Stipend Type:</strong> {{ internship.get_stipend_type_display }}</p>
   ```

---

### ⚖️ Scenario 3: Modify Business Logic Rules

**Examiner Question:** *"Restrict students so they cannot submit an application if their GPA is below 3.0."*

**Step-by-Step Fix:**
1. Open `applications/views.py`.
2. Locate `submit_application` view function.
3. Add GPA check right before creating the application record:
   ```python
   student_profile = request.user.student_profile
   if student_profile.gpa and student_profile.gpa < 3.0:
       messages.error(request, "Minimum GPA requirement of 3.0 is required to apply.")
       return redirect('internships:detail', pk=internship.id)
   ```
4. Save file and test submitting an application with GPA < 3.0.

---

### 🚨 Scenario 4: Resolving Migration Errors During Live Modification

If you add a non-nullable field without a default value, Django terminal will ask:
`Select an option to provide a default value now:`

**Quick Answer:**
- Type `1` and press Enter.
- Type `'Fixed'` or `'N/A'` (for strings) or `0` (for numbers) and press Enter.
- Then run `python manage.py migrate`.
