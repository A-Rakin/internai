# 03. Database Schema, Models & Constraints Guide

---

## 🗄️ 1. Complete Database Model Summary (16 Models)

| App Name | Model Name | Primary Key | Key Foreign Keys | Purpose / Function |
| :--- | :--- | :--- | :--- | :--- |
| `accounts` | `CustomUser` | `id` | None (Inherits `AbstractUser`) | Custom auth user (email login, role) |
| `accounts` | `StudentProfile` | `id` | `user` (1:1 `CustomUser`) | Academic info, GPA, skills, links |
| `accounts` | `CompanyProfile` | `id` | `user` (1:1 `CustomUser`) | Company name, industry, plan |
| `accounts` | `SupervisorProfile`| `id` | `user` (1:1 `CustomUser`) | Designation, department, max students |
| `internships` | `InternshipCategory`| `id` | None | Category lookup (Dev, AI, Data) |
| `internships` | `Internship` | `id` | `company` (FK `CompanyProfile`), `category` | Internship position listing |
| `internships` | `SavedInternship` | `id` | `student` (FK `CustomUser`), `internship` | Bookmarked positions |
| `applications`| `Application` | `id` | `student` (FK `CustomUser`), `internship` | Candidate application & ATS score |
| `interviews` | `Interview` | `id` | `application` (FK `Application`) | Interview scheduling & meeting links |
| `reports` | `WeeklyReport` | `id` | `student` (FK `CustomUser`), `supervisor` | Weekly activity log from student |
| `reports` | `Evaluation` | `id` | `student`, `supervisor`, `internship` | Academic final evaluation form |
| `chatbot` | `ChatSession` | `id` | `user` (FK `CustomUser`) | AI chat thread session |
| `chatbot` | `ChatMessage` | `id` | `session` (FK `ChatSession`) | Individual prompt & AI response |
| `messaging` | `Conversation` | `id` | `participants` (M2M `CustomUser`) | Direct messaging inbox thread |
| `messaging` | `Message` | `id` | `conversation` (FK), `sender` (FK) | Individual message in chat thread |
| `notifications`| `Notification` | `id` | `recipient` (FK `CustomUser`) | In-app alerts & link notifications |

---

## 📐 2. Key Relationships & Constraints in Code

### 2.1 Unique Email & Email-Based Authentication (`accounts/models.py`)
```python
class CustomUser(AbstractUser):
    email = models.EmailField('email address', unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    
    USERNAME_FIELD = 'email'  # Email is used to log in instead of username
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
```
- **Constraint:** `unique=True` ensures no two accounts can be created with the same email.

---

### 2.2 Bookmark Uniqueness (`internships/models.py`)
```python
class SavedInternship(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'internship')  # Prevents duplicate bookmarks
```
- **Constraint:** `unique_together` creates a composite database index ensuring a student cannot bookmark the same internship twice.

---

### 2.3 GPA Range Validation (`accounts/models.py`)
```python
class StudentProfile(models.Model):
    gpa = models.DecimalField(
        max_length=4, max_digits=3, decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(4.0)],
        blank=True, null=True
    )
```
- **Validation:** `MinValueValidator(0.0)` and `MaxValueValidator(4.0)` enforce valid academic GPA ranges at the Django form/model level.

---

## ⚡ 3. Database Migration Workflow (Viva Board Explanation)

- **Question:** How do database migrations work in Django?
- **Answer:**
  1. **Step 1: Write/Modify Models:** We define or edit Python classes in `models.py`.
  2. **Step 2: Generate Migration Scripts:** Running `python manage.py makemigrations` inspects changes in `models.py` and creates a versioned SQL blueprint file in `<app>/migrations/000x_...py`.
  3. **Step 3: Execute SQL in Database:** Running `python manage.py migrate` executes the unapplied migration files as SQL `CREATE TABLE` or `ALTER TABLE` statements inside MySQL/SQLite.
