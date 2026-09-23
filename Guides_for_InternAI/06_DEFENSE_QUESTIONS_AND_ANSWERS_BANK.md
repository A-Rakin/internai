# 06. Viva Board Questions & Answers Bank (35+ Q&A)

---

## ❓ Category 1: Django & Python Framework

### Q1: Why did you choose Django instead of Flask or Node.js?
- **Answer:** Django follows the "Batteries Included" philosophy. It provides built-in authentication, an advanced ORM, automatic admin interface, CSRF protection, and migration management out-of-the-box. This allowed us to focus on building complex AI features and multi-role workflows securely and rapidly.

### Q2: What is the difference between `null=True` and `blank=True` in Django models?
- **Answer:** 
  - `null=True` is a **database-level** constraint. It allows the database column to store `NULL` values.
  - `blank=True` is a **form-level / validation-level** constraint. It permits the field to be left empty in Django forms.

### Q3: How do context processors work in Django?
- **Answer:** A context processor is a Python function that executes on every request and returns a dictionary of data that is automatically merged into the template context of every rendered HTML page. In InternAI (`common/context_processors.py`), we use it to calculate unread notification and unread message counts globally for sidebar badges.

---

## 🤖 Category 2: AI Engine & Resume Parsing

### Q4: How does the AI Resume Parsing engine work?
- **Answer:** We use `pypdf` (`PdfReader`) to extract raw text from uploaded candidate PDF resumes. The text is passed into `common/ai_engine.py`, where `calculate_skill_match()` compares candidate skills, project experience, education, and format structure against internship requirements using **Groq Cloud API (Llama 3.3 70B)**.

### Q5: What happens if the Groq AI API is offline or key is missing?
- **Answer:** We implemented an automatic local fallback function `_local_skill_match()`. It executes regex keyword pattern matching against required skills so the platform continues operating seamlessly without crashing.

---

## 🗄️ Category 3: Database & Security

### Q6: How do you prevent SQL Injection attacks in InternAI?
- **Answer:** Django ORM uses parameterized queries (prepared statements) under the hood. Object lookups like `Internship.objects.filter(id=user_input)` automatically escape all user input, rendering SQL injection impossible.

### Q7: How does password hashing work in Django?
- **Answer:** Django never stores plain text passwords. When a user registers, password bytes are hashed using **PBKDF2 with SHA-256** algorithm combined with a unique salt. During login, Django hashes the entered password with the salt and compares the stored hash.

---
