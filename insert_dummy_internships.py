import os
import sys
import random
from datetime import date, timedelta

# Set up Django environment
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "internai.settings")

import django
django.setup()

from accounts.models import CustomUser, CompanyProfile
from internships.models import Internship, InternshipCategory

def run():
    print("--> Starting dummy internships insertion for 'Real Capita Group'...")

    # 1. Get or create Company user
    company_email = "hr@realcapita.com"
    user, user_created = CustomUser.objects.get_or_create(
        email=company_email,
        defaults={
            "username": "realcapitagroup",
            "first_name": "Real Capita",
            "last_name": "Group",
            "role": CustomUser.COMPANY,
            "is_active": True,
            "is_email_verified": True,
        }
    )
    if user_created:
        user.set_password("RealCapita123!")
        user.save()
        print(f"Created company user: {company_email}")

    # 2. Get or create CompanyProfile
    company_profile, prof_created = CompanyProfile.objects.get_or_create(
        user=user,
        defaults={
            "company_name": "Real Capita Group",
            "industry": "finance",
            "company_size": "201-500",
            "description": "Real Capita Group is a leading investment, real estate development, and financial solutions company in Bangladesh.",
            "website": "https://www.realcapitagroup.com",
            "address": "Level 8, Real Capita Tower, Gulshan-2, Dhaka",
            "city": "Dhaka",
            "country": "Bangladesh",
            "contact_person": "HR Manager",
            "contact_email": company_email,
            "contact_phone": "+8801711000000",
            "is_verified": True,
            "subscription_plan": "pro"
        }
    )
    if not prof_created and company_profile.company_name != "Real Capita Group":
        company_profile.company_name = "Real Capita Group"
        company_profile.is_verified = True
        company_profile.save()
    print(f"Company profile ready: {company_profile.company_name}")

    # 3. Ensure Categories exist
    categories_data = [
        ("Software Engineering", "fas fa-code"),
        ("Real Estate & Property Management", "fas fa-building"),
        ("Finance & Accounting", "fas fa-calculator"),
        ("Digital Marketing & Branding", "fas fa-bullhorn"),
        ("Business Development & Sales", "fas fa-chart-line"),
        ("Graphic Design & Multimedia", "fas fa-paint-brush"),
        ("Human Resources & Talent Management", "fas fa-users"),
        ("Data Analytics & Research", "fas fa-database"),
        ("Project Management & Operations", "fas fa-tasks"),
        ("Customer Support & Client Relations", "fas fa-headset"),
    ]

    category_objs = {}
    for cat_name, icon in categories_data:
        cat, _ = InternshipCategory.objects.get_or_create(
            name=cat_name,
            defaults={"description": f"Internship opportunities in {cat_name}", "icon": icon, "is_active": True}
        )
        category_objs[cat_name] = cat

    # 4. Generate 30 dummy internship titles and details
    titles_and_cats = [
        ("Junior Web Developer Intern", "Software Engineering"),
        ("Property Portfolio Analyst Intern", "Real Estate & Property Management"),
        ("Financial Accountant Intern", "Finance & Accounting"),
        ("Social Media & Content Marketing Intern", "Digital Marketing & Branding"),
        ("Corporate Sales & BD Intern", "Business Development & Sales"),
        ("UI/UX Design Intern", "Graphic Design & Multimedia"),
        ("HR Operations & Talent Acquisition Intern", "Human Resources & Talent Management"),
        ("Data Analyst Intern", "Data Analytics & Research"),
        ("Assistant Project Coordinator Intern", "Project Management & Operations"),
        ("Client Relations Associate Intern", "Customer Support & Client Relations"),

        ("Python / Django Backend Development Intern", "Software Engineering"),
        ("Real Estate Market Research Intern", "Real Estate & Property Management"),
        ("Investment & Risk Management Intern", "Finance & Accounting"),
        ("SEO & Growth Marketing Intern", "Digital Marketing & Branding"),
        ("B2B Enterprise Sales Intern", "Business Development & Sales"),
        ("Brand Identity & Motion Graphics Intern", "Graphic Design & Multimedia"),
        ("Employee Engagement & HR Admin Intern", "Human Resources & Talent Management"),
        ("Business Intelligence (BI) Intern", "Data Analytics & Research"),
        ("Construction Site Operations Intern", "Project Management & Operations"),
        ("Customer Success & Support Intern", "Customer Support & Client Relations"),

        ("Frontend React Developer Intern", "Software Engineering"),
        ("Commercial Property Leasing Intern", "Real Estate & Property Management"),
        ("Audit & Tax Compliance Intern", "Finance & Accounting"),
        ("Performance Marketing Specialist Intern", "Digital Marketing & Branding"),
        ("Strategic Partnerships & Expansion Intern", "Business Development & Sales"),
        ("Creative Copywriting & Content Intern", "Digital Marketing & Branding"),
        ("Recruitment & Screening Specialist Intern", "Human Resources & Talent Management"),
        ("SQL Database Admin & Analytics Intern", "Data Analytics & Research"),
        ("Supply Chain & Logistics Intern", "Project Management & Operations"),
        ("Executive Assistant & Admin Support Intern", "Project Management & Operations"),
    ]

    locations = ["Gulshan, Dhaka", "Banani, Dhaka", "Dhanmondi, Dhaka", "Uttara, Dhaka", "Agrabad, Chattogram", "Remote", "Hybrid (Gulshan, Dhaka)"]
    types = ["onsite", "hybrid", "remote"]
    durations = ["3 Months", "4 Months", "6 Months"]

    created_count = 0
    today = date.today()

    for idx, (title, cat_name) in enumerate(titles_and_cats, 1):
        cat = category_objs.get(cat_name)
        stipend_amount = random.choice([10000, 12000, 15000, 18000, 20000, 25000])
        intern_type = random.choice(types)
        loc = "Remote" if intern_type == "remote" else random.choice(locations)
        dur = random.choice(durations)
        deadline_date = today + timedelta(days=random.randint(15, 60))
        start_d = today + timedelta(days=random.randint(65, 90))

        description = (
            f"Real Capita Group is hiring a motivated {title} to join our dynamic team in {loc}. "
            f"In this role, you will work closely with industry leaders on high-impact projects, gain hands-on experience, "
            f"and contribute directly to our business operations and strategic initiatives."
        )

        requirements = (
            f"• Strong passion for {cat_name}\n"
            f"• Good verbal and written communication skills in English & Bangla\n"
            f"• Educational background in relevant field (Business, CSE, Engineering, Finance, etc.)\n"
            f"• Problem-solving mindset, self-motivated, and eager to learn."
        )

        skills = "Communication, Problem Solving, Teamwork, Analytical Thinking, Time Management"

        internship = Internship.objects.create(
            company=company_profile,
            category=cat,
            title=title,
            description=description,
            requirements=requirements,
            skills_required=skills,
            internship_type=intern_type,
            location=loc,
            duration=dur,
            stipend=stipend_amount,
            positions=random.randint(1, 5),
            status="open",
            deadline=deadline_date,
            start_date=start_d,
            is_approved=True,
            is_featured=(idx <= 5)
        )
        created_count += 1
        print(f"[{created_count}/30] Created internship: {internship.title}")

    print(f"\n--> Successfully inserted {created_count} dummy internship posts for Real Capita Group!")

if __name__ == "__main__":
    run()
