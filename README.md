# InternAI - Internship Management Platform

InternAI is a modern, AI-powered internship management system built using Django, Bootstrap 5, and vanilla CSS/JS. It supports four primary roles: **Students**, **Companies (HR)**, **Supervisors**, and **Administrators**.

---

## How to Run in Visual Studio Code (Windows)

Follow these steps to set up and run the project in VS Code:

### Step 1: Open the Project in VS Code
1. Open **Visual Studio Code**.
2. Go to **File -> Open Folder...** and select `E:\InternAi`.

### Step 2: Open a Terminal in VS Code
1. Open the integrated terminal using `Ctrl + ~` (or click **Terminal -> New Terminal** from the top menu).

### Step 3: Stop Any Running Django Server
If you already have a server running, stop it by pressing **`Ctrl + C`** in that terminal.


### Step 4: Run Database Migrations
Run these commands to generate the tables for all apps and the custom authentication system:
1. **Create Migrations**:
   ```powershell
   .\venv\Scripts\python.exe manage.py makemigrations accounts internships applications interviews reports notifications documents
   ```
2. **Apply Migrations**:
   ```powershell
   .\venv\Scripts\python.exe manage.py migrate
   ```

### Step 5: Create an Admin Superuser
To access the Admin Portal and moderate internships/users, create an admin account:
```powershell
.\venv\Scripts\python.exe manage.py createsuperuser
```
Follow the prompts in the terminal to enter your email, username, and password.

### Step 6: Start the Development Server
Launch the local Django server:
```powershell
.\venv\Scripts\python.exe manage.py runserver
```

### Step 7: Open the Web Application
Open your web browser and navigate to:
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## Project Structure & Architecture
- `accounts/`: User authentication and role-based profiles (Student, Company, Supervisor).
- `students/`: Portal for students to apply, upload resumes, and track weekly reports.
- `companies/`: Recruiter dashboard, applicant tracking, and AI ranking tools.
- `supervisors/`: Roster tracking, weekly report reviews, and evaluations.
- `administration/`: System-wide analytics and moderating controls.
- `static/`: Contains design system (`main.css`), responsive layouts (`responsive.css`), and animations.
- `templates/`: Full frontend layout including landing pages, sub-components, and dashboards.
