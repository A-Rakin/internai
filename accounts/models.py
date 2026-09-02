"""
============================================================
Accounts Models - User Authentication & Profiles
============================================================
This module defines the custom user model and role-specific profile
models for the InternAI platform. It supports four user roles:
Student, Company (HR), Supervisor, and Admin.

Models:
    - CustomUser: Extended user model with role-based authentication
    - StudentProfile: Academic and personal details for students
    - CompanyProfile: Organization details for companies
    - SupervisorProfile: Academic supervisor information
============================================================
"""

# Import Django's built-in abstract user model for extending
from django.contrib.auth.models import AbstractUser

# Import Django's model fields and utilities
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Import reverse for generating URLs from view names
from django.urls import reverse

# Import the custom user manager for handling user creation
from accounts.managers import CustomUserManager


class CustomUser(AbstractUser):
    """
    Custom User Model extending Django's AbstractUser.
    
    Adds a role field to distinguish between different user types
    (Student, Company, Supervisor, Admin). Each role has access
    to different parts of the platform.
    
    Fields inherited from AbstractUser:
        - username, email, first_name, last_name, password
        - is_active, is_staff, is_superuser, date_joined
    """

    # ---- Role Choices ----
    # Define the available user roles as constants
    STUDENT = 'student'          # Student users
    COMPANY = 'company'          # Company/HR users
    SUPERVISOR = 'supervisor'    # Academic supervisor users
    ADMIN = 'admin'              # Platform administrator users

    # Tuple of (value, display_label) pairs for the role field
    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (COMPANY, 'Company'),
        (SUPERVISOR, 'Supervisor'),
        (ADMIN, 'Admin'),
    ]

    # ---- Custom Fields ----
    # Email field - required and must be unique across all users
    email = models.EmailField(
        'email address',            # Human-readable field name
        unique=True,                 # No two users can share an email
        help_text='Required. Enter a valid email address.',
    )

    # Role field - determines which portal the user can access
    role = models.CharField(
        'user role',                 # Human-readable field name
        max_length=20,               # Maximum length of the role string
        choices=ROLE_CHOICES,        # Restrict to predefined roles
        default=STUDENT,             # Default role for new registrations
        help_text='Determines the user portal and permissions.',
    )

    # Phone number - optional contact number
    phone = models.CharField(
        'phone number',
        max_length=20,               # Supports international formats
        blank=True,                  # Not required in forms
        null=True,                   # Can be NULL in database
    )

    # Profile avatar/photo - optional profile picture
    avatar = models.ImageField(
        'profile photo',
        upload_to='avatars/',        # Upload directory within MEDIA_ROOT
        blank=True,                  # Not required
        null=True,                   # Can be NULL
    )

    # Date when the profile was last updated
    updated_at = models.DateTimeField(
        'last updated',
        auto_now=True,               # Automatically set on every save
    )

    # Whether the user's email has been verified
    is_email_verified = models.BooleanField(
        'email verified',
        default=False,               # Unverified by default
    )

    # ---- Authentication Configuration ----
    # Use email as the primary login field instead of username
    USERNAME_FIELD = 'email'

    # Fields required when creating a superuser via command line
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    # Use the custom manager for user creation
    objects = CustomUserManager()

    class Meta:
        """Model metadata options."""
        verbose_name = 'User'                    # Singular name in admin
        verbose_name_plural = 'Users'            # Plural name in admin
        ordering = ['-date_joined']              # Newest users first

    def __str__(self):
        """Return string representation of the user."""
        # Show full name if available, otherwise show email
        return self.get_full_name() or self.email

    @property
    def is_student(self):
        """Check if the user has the Student role."""
        return self.role == self.STUDENT

    @property
    def is_company(self):
        """Check if the user has the Company role."""
        return self.role == self.COMPANY

    @property
    def is_supervisor(self):
        """Check if the user has the Supervisor role."""
        return self.role == self.SUPERVISOR

    @property
    def is_admin_user(self):
        """Check if the user has the Admin role."""
        return self.role == self.ADMIN

    def get_dashboard_url(self):
        """
        Return the appropriate dashboard URL based on user role.
        Used after login to redirect users to their portal.
        """
        # Map each role to its dashboard URL name
        role_urls = {
            self.STUDENT: 'students:dashboard',
            self.COMPANY: 'companies:dashboard',
            self.SUPERVISOR: 'supervisors:dashboard',
            self.ADMIN: 'administration:dashboard',
        }
        # Return the URL for this user's role, defaulting to home
        return reverse(role_urls.get(self.role, 'landing:home'))


class StudentProfile(models.Model):
    """
    Extended profile for Student users.
    
    Contains academic information, skills, experience, and portfolio
    details that students need to present to potential employers.
    One-to-one relationship with CustomUser.
    """

    # ---- Education Level Choices ----
    EDUCATION_CHOICES = [
        ('bachelors', "Bachelor's Degree"),
        ('masters', "Master's Degree"),
        ('phd', 'PhD'),
        ('diploma', 'Diploma'),
        ('other', 'Other'),
    ]

    # ---- Relationship ----
    # One-to-one link to the CustomUser model
    # When the user is deleted, the profile is also deleted (CASCADE)
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='student_profile',  # Access via user.student_profile
        primary_key=True,                # Use user's ID as primary key
    )

    # ---- Personal Information ----
    # Date of birth for age verification
    date_of_birth = models.DateField(
        'date of birth',
        blank=True,
        null=True,
    )

    # Gender field
    gender = models.CharField(
        'gender',
        max_length=20,
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
            ('prefer_not_to_say', 'Prefer not to say'),
        ],
        blank=True,
    )

    # Address information
    address = models.TextField(
        'address',
        blank=True,
        help_text='Current residential address',
    )

    # City
    city = models.CharField('city', max_length=100, blank=True)

    # Country
    country = models.CharField('country', max_length=100, blank=True)

    # ---- Academic Information ----
    # University name
    university = models.CharField(
        'university',
        max_length=255,
        blank=True,
        help_text='Name of the university or institution',
    )

    # Department/Faculty
    department = models.CharField(
        'department',
        max_length=255,
        blank=True,
        help_text='Academic department or faculty',
    )

    # Student ID number
    student_id = models.CharField(
        'student ID',
        max_length=50,
        blank=True,
    )

    # ---- Academic Status Choices ----
    ACADEMIC_STATUS_CHOICES = [
        ('final_semester', 'Final Semester (Internship Eligible / Only Internship Remaining)'),
        ('graduated', 'Graduation Completed'),
        ('continuing', 'Continuing Studies'),
    ]

    # Education level
    education_level = models.CharField(
        'education level',
        max_length=20,
        choices=EDUCATION_CHOICES,
        blank=True,
    )

    # Academic / Internship Status (Replaces semester field)
    academic_status = models.CharField(
        'academic status',
        max_length=30,
        choices=ACADEMIC_STATUS_CHOICES,
        default='final_semester',
        help_text='Indicates whether only the internship semester remains for graduation.',
    )

    # Deprecated legacy field (kept for migration safety)
    current_semester = models.CharField(
        'current semester',
        max_length=20,
        blank=True,
        default='',
    )

    # GPA/CGPA (Strictly constrained to 0.00 - 4.00 scale)
    gpa = models.DecimalField(
        'GPA/CGPA',
        max_digits=4,        # Total digits (e.g., 3.95)
        decimal_places=2,    # Digits after decimal point
        blank=True,
        null=True,
        validators=[MinValueValidator(0.00), MaxValueValidator(4.00)],
        help_text='Cumulative Grade Point Average (0.00 - 4.00 scale)',
    )

    # Expected graduation date
    expected_graduation = models.DateField(
        'expected graduation',
        blank=True,
        null=True,
    )

    # Assigned Academic Supervisor
    supervisor = models.ForeignKey(
        'SupervisorProfile',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='supervised_students',
        verbose_name='academic supervisor',
    )

    # ---- Skills & Experience ----
    # Technical skills (stored as comma-separated values)
    skills = models.TextField(
        'technical skills',
        blank=True,
        help_text='Comma-separated list of skills (e.g., Python, JavaScript, React)',
    )

    # Work experience summary
    experience = models.TextField(
        'work experience',
        blank=True,
        help_text='Brief description of previous work experience',
    )

    # Languages spoken
    languages = models.CharField(
        'languages',
        max_length=255,
        blank=True,
        help_text='Languages spoken (e.g., English, Bangla)',
    )

    # ---- Portfolio & Links ----
    # LinkedIn profile URL
    linkedin_url = models.URLField(
        'LinkedIn profile',
        blank=True,
    )

    # GitHub profile URL
    github_url = models.URLField(
        'GitHub profile',
        blank=True,
    )

    # Portfolio website URL
    portfolio_url = models.URLField(
        'portfolio website',
        blank=True,
    )

    # ---- Bio ----
    # Short biography or about section
    bio = models.TextField(
        'biography',
        max_length=1000,
        blank=True,
        help_text='A short bio about yourself (max 1000 characters)',
    )

    # ---- Timestamps ----
    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)

    class Meta:
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'

    def __str__(self):
        """Return string representation."""
        return f"Student: {self.user.get_full_name()}"

    @property
    def profile_completion(self):
        """
        Calculate the profile completion percentage.
        Checks which fields are filled and returns a percentage.
        """
        # List of fields to check for completion
        fields_to_check = [
            self.user.first_name, self.user.last_name, self.user.phone,
            self.user.avatar, self.university, self.department,
            self.education_level, self.skills, self.bio,
            self.linkedin_url, self.github_url,
        ]
        # Count filled fields (non-empty, non-None)
        filled = sum(1 for f in fields_to_check if f)
        # Calculate percentage
        return int((filled / len(fields_to_check)) * 100)

    def get_skills_list(self):
        """Return skills as a list of strings."""
        if self.skills:
            return [s.strip() for s in self.skills.split(',')]
        return []


class CompanyProfile(models.Model):
    """
    Extended profile for Company/HR users.
    
    Contains organization details, industry classification,
    and contact information for companies offering internships.
    """

    # ---- Industry Choices ----
    INDUSTRY_CHOICES = [
        ('technology', 'Technology'),
        ('finance', 'Finance & Banking'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education'),
        ('manufacturing', 'Manufacturing'),
        ('retail', 'Retail'),
        ('consulting', 'Consulting'),
        ('media', 'Media & Entertainment'),
        ('telecom', 'Telecommunications'),
        ('energy', 'Energy'),
        ('government', 'Government'),
        ('nonprofit', 'Non-Profit'),
        ('other', 'Other'),
    ]

    # ---- Company Size Choices ----
    SIZE_CHOICES = [
        ('1-10', '1-10 employees'),
        ('11-50', '11-50 employees'),
        ('51-200', '51-200 employees'),
        ('201-500', '201-500 employees'),
        ('501-1000', '501-1000 employees'),
        ('1000+', '1000+ employees'),
    ]

    # ---- Relationship ----
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='company_profile',
        primary_key=True,
    )

    # ---- Company Information ----
    # Official company name
    company_name = models.CharField(
        'company name',
        max_length=255,
    )

    # Company logo image
    logo = models.ImageField(
        'company logo',
        upload_to='company_logos/',
        blank=True,
        null=True,
    )

    # Industry classification
    industry = models.CharField(
        'industry',
        max_length=50,
        choices=INDUSTRY_CHOICES,
        blank=True,
    )

    # Company size
    company_size = models.CharField(
        'company size',
        max_length=20,
        choices=SIZE_CHOICES,
        blank=True,
    )

    # Company description/about
    description = models.TextField(
        'company description',
        blank=True,
        help_text='Brief description of the company',
    )

    # Official website
    website = models.URLField(
        'company website',
        blank=True,
    )

    # ---- Address ----
    address = models.TextField('office address', blank=True)
    city = models.CharField('city', max_length=100, blank=True)
    country = models.CharField('country', max_length=100, blank=True)

    # ---- Contact ----
    # HR contact person name
    contact_person = models.CharField(
        'contact person',
        max_length=255,
        blank=True,
        help_text='Name of the HR contact person',
    )

    # HR contact email
    contact_email = models.EmailField(
        'contact email',
        blank=True,
    )

    # HR contact phone
    contact_phone = models.CharField(
        'contact phone',
        max_length=20,
        blank=True,
    )

    # ---- Subscription Plan Choices ----
    PLAN_CHOICES = [
        ('basic', 'Basic Free ($0/mo)'),
        ('pro', 'Pro Recruiter ($20/mo)'),
        ('ultimate', 'Ultimate Enterprise ($80/mo)'),
    ]

    # ---- Verification & Subscription ----
    # Whether the company has been verified by admin
    is_verified = models.BooleanField(
        'verified',
        default=False,
        help_text='Whether the company has been verified by administrators',
    )

    # Active subscription plan
    subscription_plan = models.CharField(
        'subscription plan',
        max_length=20,
        choices=PLAN_CHOICES,
        default='basic',
    )

    # ---- Timestamps ----
    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)

    class Meta:
        verbose_name = 'Company Profile'
        verbose_name_plural = 'Company Profiles'

    def __str__(self):
        """Return company name as string representation."""
        return self.company_name or f"Company: {self.user.email}"


class SupervisorProfile(models.Model):
    """
    Extended profile for Academic Supervisor users.
    
    Contains university, department, and expertise information
    for supervisors who monitor student internships.
    """

    # ---- Designation Choices ----
    DESIGNATION_CHOICES = [
        ('professor', 'Professor'),
        ('associate_professor', 'Associate Professor'),
        ('assistant_professor', 'Assistant Professor'),
        ('lecturer', 'Lecturer'),
        ('senior_lecturer', 'Senior Lecturer'),
        ('adjunct', 'Adjunct Faculty'),
        ('other', 'Other'),
    ]

    # ---- Relationship ----
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='supervisor_profile',
        primary_key=True,
    )

    # ---- Academic Information ----
    # University name
    university = models.CharField(
        'university',
        max_length=255,
        blank=True,
    )

    # Department
    department = models.CharField(
        'department',
        max_length=255,
        blank=True,
    )

    # Designation/Title
    designation = models.CharField(
        'designation',
        max_length=50,
        choices=DESIGNATION_CHOICES,
        blank=True,
    )

    # Employee ID
    employee_id = models.CharField(
        'employee ID',
        max_length=50,
        blank=True,
    )

    # Areas of expertise
    expertise = models.TextField(
        'areas of expertise',
        blank=True,
        help_text='Comma-separated list of expertise areas',
    )

    # Maximum number of students to supervise
    max_students = models.PositiveIntegerField(
        'maximum students',
        default=10,
        help_text='Maximum number of students this supervisor can handle',
    )

    # Bio/About
    bio = models.TextField(
        'biography',
        max_length=1000,
        blank=True,
    )

    # ---- Timestamps ----
    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)

    class Meta:
        verbose_name = 'Supervisor Profile'
        verbose_name_plural = 'Supervisor Profiles'

    def __str__(self):
        """Return string representation with designation."""
        return f"Supervisor: {self.user.get_full_name()}"

    def get_expertise_list(self):
        """Return expertise areas as a list of strings."""
        if self.expertise:
            return [e.strip() for e in self.expertise.split(',')]
        return []
