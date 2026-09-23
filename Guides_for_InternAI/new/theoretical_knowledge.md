# InternAI - Complete Django & Web Engineering Theoretical Knowledge Guide

This master guide covers all theoretical concepts, architecture, file structures, Django ORM mechanics, commands, and internals used in **InternAI**. Use this for rapid review and viva preparation.

---

## 1. Django Architectural Pattern: MVT (Model-View-Template)

Django follows the **MVT (Model-View-Template)** architecture, which is a software design pattern that separates concerns into three distinct layers:

```
                  +-----------------------------------+
                  |           User Request            |
                  +-----------------------------------+
                                    |
                                    v
                          [ URL Dispatcher ]
                                    |
                                    v
                               [ View ] <======> [ Model ] <===> [ Database ]
                                    |
                                    v
                               [ Template ]
                                    |
                                    v
                  +-----------------------------------+
                  |           HTTP Response           |
                  +-----------------------------------+
```

### MVT Component Comparison with standard MVC:
1. **Model (`models.py`)**:
   - Manages data structure, business logic, validation rules, and database interactions using Django ORM.
   - *Equivalent to*: Model in MVC.
2. **View (`views.py`)**:
   - Contains business logic that receives HTTP requests, interacts with Models to query data, and renders Templates or returns JSON.
   - *Equivalent to*: Controller in MVC.
3. **Template (`templates/`)**:
   - Controls presentation logic and layout using Django Template Language (DTL) tags (`{% %}`) and variables (`{{ }}`).
   - *Equivalent to*: View in MVC.

---

## 2. Web Request-Response Lifecycle in Django

When a student clicks "Apply Now" or navigates to `/applications/` in InternAI, the request flows as follows:

1. **WSGI / ASGI Server**: Receives raw HTTP request from browser (e.g., Gunicorn or Django runserver).
2. **Settings Initialization**: Loads `settings.py` configuration (middleware, database configs, app registries).
3. **Middleware Execution (Request Phase)**: Passes request through global middleware chain (e.g., `SecurityMiddleware`, `SessionMiddleware`, `AuthenticationMiddleware`, `CsrfViewMiddleware`).
4. **URL Dispatcher (`urls.py`)**: Matches requested URL path against patterns registered in root `urls.py` and included app `urls.py`.
5. **View Function Execution (`views.py`)**:
   - Verifies permissions & decorators (e.g., `@login_required`).
   - Executes Django ORM queries against Database (SQLite / PostgreSQL / MySQL).
6. **Template Rendering**: Combines query dataset with template HTML file using Django Template Engine.
7. **Middleware Execution (Response Phase)**: Passes generated response back through middleware chain.
8. **HTTP Response**: Returns standard HTML document / JSON response to user browser with HTTP status code (200 OK, 302 Redirect, 404 Not Found, etc.).

---

## 3. Django App Directory & Essential File Roles

Each app inside InternAI (e.g., `accounts/`, `applications/`, `internships/`, `analytics/`) follows a standardized structure:

| File Name | Purpose & Practical Role in InternAI |
| :--- | :--- |
| `__init__.py` | Marks the directory as a Python package. Tells Python that this folder contains importable modules. |
| `apps.py` | Configures app metadata (e.g., `ApplicationsConfig`, app name, default auto field type). |
| `models.py` | Defines database table schemas as Python classes using `models.Model`. |
| `views.py` | Python functions/classes handling business logic, database queries, and template responses. |
| `urls.py` | Maps specific URL endpoints to view functions within the app. |
| `admin.py` | Registers app models with Django's built-in Admin Portal for CRUD management. |
| `forms.py` | Defines HTML form handling, field validation rules, and model form mappings. |
| `signals.py` | Decoupled event listeners (e.g., automatically creating a profile when a CustomUser is registered). |
| `migrations/` | Directory containing Python scripts tracking model changes to convert into SQL DDL statements. |

---

## 4. Root Configuration Files (`internai/`)

1. **`settings.py`**:
   - `INSTALLED_APPS`: List of active Django modules and custom apps (`accounts`, `applications`, `analytics`, etc.).
   - `MIDDLEWARE`: Pluggable request/response processing hooks.
   - `DATABASES`: Database engine, host, port, credentials configuration.
   - `STATIC_URL` & `MEDIA_URL`: Routing for CSS/JS assets and user-uploaded files (resumes, avatars).
2. **`urls.py`**:
   - Global URL router using `path()` and `include()` to route traffic to app-level `urls.py`.
3. **`wsgi.py` / `asgi.py`**:
   - Entry point for Web Server Gateway Interface (WSGI) or Asynchronous Server Gateway Interface (ASGI) deployment.

---

## 5. Django ORM (Object-Relational Mapping) Deep-Dive

Django ORM converts Python code into SQL queries automatically, eliminating raw SQL vulnerabilities.

### Key ORM Operations & Code Examples in InternAI

#### A. Filtering & Lookups
```python
# Exact match lookup
open_internships = Internship.objects.filter(status='open', is_approved=True)

# Field lookups (__contains, __gte, __in)
tech_jobs = Internship.objects.filter(title__icontains='Developer')
high_match = Application.objects.filter(ai_match_score__gte=80)
```

#### B. Complex Queries: `Q` Objects & `F` Expressions
```python
from django.db.models import Q, F

# OR condition query
results = Internship.objects.filter(Q(location='Remote') | Q(location='Dhaka'))

# F expression (Database-level value update without loading into Python memory)
Internship.objects.filter(id=5).update(views_count=F('views_count') + 1)
```

#### C. Query Optimization: `select_related` vs `prefetch_related`
- **`select_related(*fields)`**:
  - Uses SQL `JOIN` clause. Best for **Single-Value Relationships** (`ForeignKey` and `OneToOneField`).
  - *Example*: `Application.objects.select_related('student__user', 'internship')` (1 single JOIN query).
- **`prefetch_related(*lookups)`**:
  - Executes separate queries and joins them in Python memory. Best for **Multi-Value Relationships** (`ManyToManyField` and reverse ForeignKeys).
  - *Example*: `InternshipCategory.objects.prefetch_related('internships')`.

#### D. Aggregation vs Annotation
- **`aggregate()`**: Returns a dictionary of summary values calculated over the entire QuerySet.
  ```python
  avg_score = Application.objects.aggregate(Avg('ai_match_score'))
  # Output: {'ai_match_score__avg': 78.5}
  ```
- **`annotate()`**: Adds calculated values to each object in the QuerySet (similar to SQL `GROUP BY`).
  ```python
  categories = InternshipCategory.objects.annotate(count=Count('internships'))
  # Each category object gets a .count attribute
  ```

---

## 6. Crucial Django Management Commands

Run these commands using `python manage.py <command>` in terminal:

| Command | Action |
| :--- | :--- |
| `python manage.py runserver` | Starts local development server at `http://127.0.0.1:8000/`. |
| `python manage.py makemigrations` | Detects changes in `models.py` and creates new migration file scripts in `migrations/`. |
| `python manage.py migrate` | Executes pending migration scripts to update database tables. |
| `python manage.py createsuperuser` | Prompts terminal input to create an administrative root user. |
| `python manage.py collectstatic` | Gathers static files from all apps into a single directory for deployment. |
| `python manage.py shell` | Opens interactive Python shell initialized with Django environment and models. |
| `python create_dummy_profiles.py` | Custom project script to seed system with sample students, companies, and supervisors. |

---

## 7. Authentication, Permissions & Security in Django

1. **Custom User Model (`accounts/models.py`)**:
   - Inherits from `AbstractUser`.
   - Defines custom `role` field: `student`, `company`, `supervisor`, `admin`.
2. **Role-Based Access Control (RBAC)**:
   - Enforced in `views.py` using decorators (`@login_required`) and role checking (`if request.user.role == 'student'`).
3. **Security Protections**:
   - **CSRF Protection**: Tokens embedded in forms via `{% csrf_token %}` to block cross-site request forgery.
   - **SQL Injection Prevention**: Django ORM parameterizes queries automatically.
   - **XSS Protection**: Django Template Language auto-escapes HTML characters in rendered variables.
