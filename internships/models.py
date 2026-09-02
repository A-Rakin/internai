"""
============================================================
Internships Models - Internship Listings
============================================================
Models for managing internship positions posted by companies,
including categories, requirements, and status tracking.
============================================================
"""

from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from accounts.models import CompanyProfile


class InternshipCategory(models.Model):
    """
    Category classification for internships.
    Examples: Software Development, Data Science, Marketing, etc.
    """
    # Category name - must be unique
    name = models.CharField('category name', max_length=100, unique=True)

    # Optional description of the category
    description = models.TextField('description', blank=True)

    # Icon class name for display (e.g., 'fas fa-code')
    icon = models.CharField('icon class', max_length=50, blank=True)

    # Category icon image file
    image = models.ImageField('category image', upload_to='category_icons/', blank=True, null=True)

    # Whether this category is active and visible
    is_active = models.BooleanField('active', default=True)

    # Timestamps
    created_at = models.DateTimeField('created at', auto_now_add=True)

    class Meta:
        verbose_name = 'Internship Category'
        verbose_name_plural = 'Internship Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Internship(models.Model):
    """
    Internship listing posted by a company.
    
    Contains all details about an internship position including
    title, description, requirements, duration, stipend, and status.
    """

    # ---- Status Choices ----
    STATUS_CHOICES = [
        ('draft', 'Draft'),             # Not yet published
        ('open', 'Open'),               # Accepting applications
        ('closed', 'Closed'),           # No longer accepting
        ('filled', 'Filled'),           # Position has been filled
        ('cancelled', 'Cancelled'),     # Cancelled by company
    ]

    # ---- Type Choices ----
    TYPE_CHOICES = [
        ('onsite', 'On-site'),          # Work at company office
        ('remote', 'Remote'),           # Work from home
        ('hybrid', 'Hybrid'),           # Mix of onsite and remote
    ]

    # ---- Relationships ----
    # The company offering this internship
    company = models.ForeignKey(
        CompanyProfile,
        on_delete=models.CASCADE,
        related_name='internships',
        verbose_name='company',
    )

    # Category classification
    category = models.ForeignKey(
        InternshipCategory,
        on_delete=models.SET_NULL,      # Keep internship if category deleted
        related_name='internships',
        verbose_name='category',
        blank=True,
        null=True,
    )

    # ---- Basic Information ----
    # Internship title (e.g., "Frontend Developer Intern")
    title = models.CharField('title', max_length=255)

    # Detailed description of the internship
    description = models.TextField(
        'description',
        help_text='Detailed description of the internship role and responsibilities',
    )

    # Required qualifications and skills
    requirements = models.TextField(
        'requirements',
        help_text='Skills and qualifications required for this position',
    )

    # Required skills (comma-separated for filtering)
    skills_required = models.TextField(
        'required skills',
        blank=True,
        help_text='Comma-separated list of required skills',
    )

    # ---- Position Details ----
    # Internship type (onsite/remote/hybrid)
    internship_type = models.CharField(
        'type',
        max_length=20,
        choices=TYPE_CHOICES,
        default='onsite',
    )

    # Location (city, country)
    location = models.CharField('location', max_length=255, blank=True)

    # Duration of the internship
    duration = models.CharField(
        'duration',
        max_length=100,
        help_text='e.g., 3 months, 6 months',
    )

    # Monthly stipend/salary
    stipend = models.DecimalField(
        'monthly stipend',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text='Monthly stipend amount in BDT',
    )

    # Number of positions available
    positions = models.PositiveIntegerField(
        'positions available',
        default=1,
        validators=[MinValueValidator(1)],
    )

    # ---- Status & Dates ----
    # Current status of the internship listing
    status = models.CharField(
        'status',
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
    )

    # Application deadline
    deadline = models.DateField(
        'application deadline',
        help_text='Last date to submit applications',
    )

    # Start date of the internship
    start_date = models.DateField('start date', blank=True, null=True)

    # Whether the listing has been approved by admin
    is_approved = models.BooleanField('approved', default=False)

    # Whether the listing is featured/highlighted
    is_featured = models.BooleanField('featured', default=False)

    # ---- View Count ----
    views_count = models.PositiveIntegerField('views', default=0)

    # ---- Timestamps ----
    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)

    class Meta:
        verbose_name = 'Internship'
        verbose_name_plural = 'Internships'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} at {self.company.company_name}"

    def get_absolute_url(self):
        """Return URL to view this internship's detail page."""
        return reverse('internships:detail', kwargs={'pk': self.pk})

    def get_skills_list(self):
        """Return required skills as a list."""
        if self.skills_required:
            return [s.strip() for s in self.skills_required.split(',')]
        return []

    @property
    def is_open(self):
        """Check if the internship is currently accepting applications."""
        return self.status == 'open' and self.is_approved


class SavedInternship(models.Model):
    """
    Bookmark / saved internship by a student.
    """
    student = models.ForeignKey(
        'accounts.StudentProfile',
        on_delete=models.CASCADE,
        related_name='saved_internships',
        verbose_name='student',
    )
    internship = models.ForeignKey(
        Internship,
        on_delete=models.CASCADE,
        related_name='saved_by_students',
        verbose_name='internship',
    )
    saved_at = models.DateTimeField('saved at', auto_now_add=True)

    class Meta:
        verbose_name = 'Saved Internship'
        verbose_name_plural = 'Saved Internships'
        unique_together = ['student', 'internship']
        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.student.user.get_full_name()} saved {self.internship.title}"

