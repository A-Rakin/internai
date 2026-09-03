import os
import sys

# Set up Django environment
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "internai.settings")

import django
django.setup()

from accounts.models import CustomUser, StudentProfile, SupervisorProfile, CompanyProfile

def create_profiles():
    print("==================================================")
    print("   Creating Dummy Profiles (Students, Supervisors, Companies)")
    print("==================================================")

    # ---------------------------------------------------------
    # 1. CREATE 10 STUDENT PROFILES
    # ---------------------------------------------------------
    students_data = [
        {"email": "student1@internai.com", "username": "student_rahim", "first": "Rahim", "last": "Uddin", "university": "University of Dhaka", "dept": "Computer Science & Engineering", "sid": "DU-CSE-2021001", "gpa": 3.82, "skills": "Python, Django, PostgreSQL, HTML/CSS"},
        {"email": "student2@internai.com", "username": "student_fatima", "first": "Fatima", "last": "Zahra", "university": "BUET", "dept": "Electrical & Electronic Engineering", "sid": "BUET-EEE-2021045", "gpa": 3.90, "skills": "C++, MATLAB, Embedded Systems, Circuit Design"},
        {"email": "student3@internai.com", "username": "student_tanvir", "first": "Tanvir", "last": "Hasan", "university": "North South University", "dept": "Business Administration", "sid": "NSU-BBA-2021112", "gpa": 3.65, "skills": "Digital Marketing, Financial Modeling, MS Excel"},
        {"email": "student4@internai.com", "username": "student_nusrat", "first": "Nusrat", "last": "Jahan", "university": "BRAC University", "dept": "Computer Science & Engineering", "sid": "BRAC-CSE-2021089", "gpa": 3.78, "skills": "React.js, JavaScript, Node.js, UI/UX Design"},
        {"email": "student5@internai.com", "username": "student_mahmud", "first": "Mahmudul", "last": "Karim", "university": "Islamic University of Technology", "dept": "Software Engineering", "sid": "IUT-SWE-2021004", "gpa": 3.88, "skills": "Java, Spring Boot, Docker, REST APIs"},
        {"email": "student6@internai.com", "username": "student_anika", "first": "Anika", "last": "Rahman", "university": "MIST", "dept": "Computer Science & Engineering", "sid": "MIST-CSE-2021019", "gpa": 3.72, "skills": "Python, Machine Learning, TensorFlow, Pandas"},
        {"email": "student7@internai.com", "username": "student_shahriar", "first": "Shahriar", "last": "Kabir", "university": "SUST", "dept": "Computer Science & Engineering", "sid": "SUST-CSE-2021053", "gpa": 3.60, "skills": "C++, Data Structures, Algorithms, Linux"},
        {"email": "student8@internai.com", "username": "student_farhana", "first": "Farhana", "last": "Yasmin", "university": "AIUB", "dept": "Software Engineering", "sid": "AIUB-SE-2021077", "gpa": 3.55, "skills": "PHP, Laravel, MySQL, Front-end Web"},
        {"email": "student9@internai.com", "username": "student_sabbir", "first": "Sabbir", "last": "Ahmed", "university": "United International University", "dept": "Data Science", "sid": "UIU-DS-2021031", "gpa": 3.80, "skills": "SQL, R, Python, PowerBI, Data Visualization"},
        {"email": "student10@internai.com", "username": "student_mehedi", "first": "Mehedi", "last": "Hasan", "university": "RUET", "dept": "Electrical & Electronic Engineering", "sid": "RUET-EEE-2021062", "gpa": 3.68, "skills": "PLC Programming, IoT, Arduino, Python"}
    ]

    student_password = "Student123!"
    created_students = []

    print("\n--- Creating Student Accounts & Profiles ---")
    for s in students_data:
        user, created = CustomUser.objects.get_or_create(
            email=s["email"],
            defaults={
                "username": s["username"],
                "first_name": s["first"],
                "last_name": s["last"],
                "role": CustomUser.STUDENT,
                "is_active": True,
                "is_email_verified": True
            }
        )
        user.set_password(student_password)
        user.save()

        profile, p_created = StudentProfile.objects.get_or_create(
            user=user,
            defaults={
                "university": s["university"],
                "department": s["dept"],
                "student_id": s["sid"],
                "gpa": s["gpa"],
                "education_level": "bachelors",
                "academic_status": "final_semester",
                "skills": s["skills"],
                "bio": f"Enthusiastic {s['dept']} student at {s['university']} looking for an internship opportunity."
            }
        )
        created_students.append((user.email, student_password, user.get_full_name(), s["university"]))
        print(f"  [Student] {user.get_full_name()} ({user.email}) - {'Created' if created else 'Updated Password'}")

    # ---------------------------------------------------------
    # 2. CREATE 10 SUPERVISOR PROFILES
    # ---------------------------------------------------------
    supervisors_data = [
        {"email": "supervisor1@internai.com", "username": "prof_rashid", "first": "Dr. M. A.", "last": "Rashid", "university": "University of Dhaka", "dept": "Computer Science & Engineering", "designation": "professor", "empid": "DU-FAC-0101", "expertise": "Artificial Intelligence, Data Mining, Software Engineering"},
        {"email": "supervisor2@internai.com", "username": "prof_shamsul", "first": "Dr. Shamsul", "last": "Alam", "university": "BUET", "dept": "Electrical & Electronic Engineering", "designation": "professor", "empid": "BUET-FAC-0052", "expertise": "Power Systems, Telecommunications, Signal Processing"},
        {"email": "supervisor3@internai.com", "username": "dr_tariq", "first": "Dr. Tariq", "last": "Mahmud", "university": "North South University", "dept": "Computer Science & Engineering", "designation": "associate_professor", "empid": "NSU-FAC-0219", "expertise": "Cyber Security, Network Protocol, Web Engineering"},
        {"email": "supervisor4@internai.com", "username": "prof_syeda", "first": "Dr. Syeda", "last": "Naznin", "university": "BRAC University", "dept": "Computer Science & Engineering", "designation": "professor", "empid": "BRAC-FAC-0144", "expertise": "Human-Computer Interaction, Cloud Computing"},
        {"email": "supervisor5@internai.com", "username": "dr_monirul", "first": "Dr. Monirul", "last": "Islam", "university": "Islamic University of Technology", "dept": "Software Engineering", "designation": "associate_professor", "empid": "IUT-FAC-0087", "expertise": "Distributed Systems, Software Testing, DevOps"},
        {"email": "supervisor6@internai.com", "username": "dr_kazi", "first": "Dr. Kazi", "last": "Rafiqul", "university": "MIST", "dept": "Computer Science & Engineering", "designation": "assistant_professor", "empid": "MIST-FAC-0312", "expertise": "Computer Vision, Embedded AI, Mobile App Dev"},
        {"email": "supervisor7@internai.com", "username": "prof_naimul", "first": "Dr. Naimul", "last": "Haque", "university": "SUST", "dept": "Computer Science & Engineering", "designation": "professor", "empid": "SUST-FAC-0015", "expertise": "Natural Language Processing, Machine Learning"},
        {"email": "supervisor8@internai.com", "username": "dr_rezwan", "first": "Dr. Rezwan", "last": "Ahmed", "university": "AIUB", "dept": "Computer Science", "designation": "senior_lecturer", "empid": "AIUB-FAC-0402", "expertise": "Full-stack Web Dev, Database Management"},
        {"email": "supervisor9@internai.com", "username": "dr_farzana", "first": "Dr. Farzana", "last": "Chowdhury", "university": "United International University", "dept": "Data Science", "designation": "associate_professor", "empid": "UIU-FAC-0198", "expertise": "Big Data Analytics, Predictive Modeling"},
        {"email": "supervisor10@internai.com", "username": "prof_hasanul", "first": "Dr. Hasanul", "last": "Banna", "university": "RUET", "dept": "Electrical & Electronic Engineering", "designation": "professor", "empid": "RUET-FAC-0033", "expertise": "Renewable Energy, Robotics, Automation"}
    ]

    supervisor_password = "Supervisor123!"
    created_supervisors = []

    print("\n--- Creating Supervisor Accounts & Profiles ---")
    for sup in supervisors_data:
        user, created = CustomUser.objects.get_or_create(
            email=sup["email"],
            defaults={
                "username": sup["username"],
                "first_name": sup["first"],
                "last_name": sup["last"],
                "role": CustomUser.SUPERVISOR,
                "is_active": True,
                "is_email_verified": True
            }
        )
        user.set_password(supervisor_password)
        user.save()

        profile, p_created = SupervisorProfile.objects.get_or_create(
            user=user,
            defaults={
                "university": sup["university"],
                "department": sup["dept"],
                "designation": sup["designation"],
                "employee_id": sup["empid"],
                "expertise": sup["expertise"],
                "max_students": 10,
                "bio": f"{sup['designation'].replace('_', ' ').title()} in {sup['dept']} at {sup['university']}."
            }
        )
        created_supervisors.append((user.email, supervisor_password, user.get_full_name(), sup["university"]))
        print(f"  [Supervisor] {user.get_full_name()} ({user.email}) - {'Created' if created else 'Updated Password'}")

    # ---------------------------------------------------------
    # 3. CREATE 10 COMPANY PROFILES
    # ---------------------------------------------------------
    companies_data = [
        {"email": "company1@internai.com", "username": "techcraft_ltd", "name": "TechCraft Solutions Ltd.", "industry": "technology", "size": "51-200", "city": "Dhaka", "desc": "Leading custom software development and cloud solution provider in Bangladesh."},
        {"email": "company2@internai.com", "username": "dataverse_tech", "name": "DataVerse Technologies", "industry": "technology", "size": "11-50", "city": "Dhaka", "desc": "Specializing in enterprise data analytics, AI products, and business intelligence."},
        {"email": "company3@internai.com", "username": "fintech_innovations", "name": "FinTech Innovations Ltd.", "industry": "finance", "size": "201-500", "city": "Dhaka", "desc": "Next-gen payment gateways and digital financial solutions provider."},
        {"email": "company4@internai.com", "username": "apex_systems", "name": "Apex Systems & Logistics", "industry": "consulting", "size": "51-200", "city": "Chattogram", "desc": "Supply chain optimization, logistics management, and business consultancy."},
        {"email": "company5@internai.com", "username": "greencloud_soft", "name": "GreenCloud Software Inc.", "industry": "technology", "size": "11-50", "city": "Dhaka", "desc": "SaaS startup focused on sustainable green computing and cloud automation."},
        {"email": "company6@internai.com", "username": "digitalreach_media", "name": "DigitalReach Media & Marketing", "industry": "media", "size": "51-200", "city": "Dhaka", "desc": "Full-service digital marketing agency, growth hacking, and creative branding."},
        {"email": "company7@internai.com", "username": "nextgen_robotics", "name": "NextGen Robotics & AI Labs", "industry": "technology", "size": "1-10", "city": "Dhaka", "desc": "Cutting-edge research & development firm building IoT and industrial robotics solutions."},
        {"email": "company8@internai.com", "username": "healthpulse_tech", "name": "HealthPulse Technologies", "industry": "healthcare", "size": "51-200", "city": "Dhaka", "desc": "Digital health ecosystem, telemedicine software, and hospital management platforms."},
        {"email": "company9@internai.com", "username": "cybershield_sec", "name": "CyberShield Security Ltd.", "industry": "technology", "size": "11-50", "city": "Dhaka", "desc": "Cybersecurity audit, penetration testing, and enterprise infrastructure protection."},
        {"email": "company10@internai.com", "username": "smartedu_global", "name": "SmartEdu Global Tech", "industry": "education", "size": "51-200", "city": "Dhaka", "desc": "EdTech platform connecting students with global learning resources and universities."}
    ]

    company_password = "Company123!"
    created_companies = []

    print("\n--- Creating Company Accounts & Profiles ---")
    for c in companies_data:
        user, created = CustomUser.objects.get_or_create(
            email=c["email"],
            defaults={
                "username": c["username"],
                "first_name": c["name"],
                "last_name": "",
                "role": CustomUser.COMPANY,
                "is_active": True,
                "is_email_verified": True
            }
        )
        user.set_password(company_password)
        user.save()

        profile, p_created = CompanyProfile.objects.get_or_create(
            user=user,
            defaults={
                "company_name": c["name"],
                "industry": c["industry"],
                "company_size": c["size"],
                "description": c["desc"],
                "website": f"https://www.{c['username']}.com",
                "address": f"Tower 4, Road 11, {c['city']}",
                "city": c["city"],
                "country": "Bangladesh",
                "contact_person": "HR Operations",
                "contact_email": c["email"],
                "contact_phone": "+8801700000000",
                "is_verified": True,
                "subscription_plan": "pro"
            }
        )
        created_companies.append((user.email, company_password, c["name"], c["industry"].capitalize()))
        print(f"  [Company] {c['name']} ({user.email}) - {'Created' if created else 'Updated Password'}")

    print("\n==================================================")
    print("   Summary of Created Credentials")
    print("==================================================")
    print("\nSTUDENT CREDENTIALS (Password: Student123!):")
    for email, pwd, name, uni in created_students:
        print(f"  - Email: {email:<25} | Name: {name:<20} | Uni: {uni}")

    print("\nSUPERVISOR CREDENTIALS (Password: Supervisor123!):")
    for email, pwd, name, uni in created_supervisors:
        print(f"  - Email: {email:<25} | Name: {name:<20} | Uni: {uni}")

    print("\nCOMPANY CREDENTIALS (Password: Company123!):")
    for email, pwd, name, ind in created_companies:
        print(f"  - Email: {email:<25} | Company: {name:<30} | Industry: {ind}")

if __name__ == "__main__":
    create_profiles()
