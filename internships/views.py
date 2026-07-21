"""
============================================================
Internships Views - Public & Student Internship Browsing
============================================================
"""

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from internships.models import Internship, InternshipCategory
from applications.models import Application
from accounts.models import StudentProfile


def browse(request):
    """Browse all open and approved internships."""
    category_id = request.GET.get('category', '')
    type_filter = request.GET.get('type', '')
    search_query = request.GET.get('q', '')

    internships = Internship.objects.filter(is_approved=True, status='open').select_related('company', 'category')

    if category_id:
        internships = internships.filter(category_id=category_id)
    if type_filter:
        internships = internships.filter(internship_type=type_filter)
    if search_query:
        internships = internships.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(company__company_name__icontains=search_query) |
            Q(skills_required__icontains=search_query)
        )

    categories = InternshipCategory.objects.filter(is_active=True)

    applied_ids = []
    if request.user.is_authenticated and hasattr(request.user, 'student_profile'):
        applied_ids = Application.objects.filter(
            student=request.user.student_profile
        ).values_list('internship_id', flat=True)

    context = {
        'internships': internships.order_by('-created_at'),
        'categories': categories,
        'selected_category': category_id,
        'selected_type': type_filter,
        'search_query': search_query,
        'applied_ids': applied_ids,
    }
    return render(request, 'internships/browse.html', context)


def detail(request, pk=None):
    """View detailed single internship listing."""
    internship = get_object_or_404(Internship, pk=pk)

    # Increment view count
    internship.views_count += 1
    internship.save(update_fields=['views_count'])

    has_applied = False
    if request.user.is_authenticated and hasattr(request.user, 'student_profile'):
        has_applied = Application.objects.filter(
            student=request.user.student_profile,
            internship=internship
        ).exists()

    context = {
        'internship': internship,
        'has_applied': has_applied,
    }
    return render(request, 'internships/detail.html', context)


def search_results(request):
    """Search internships endpoint."""
    return browse(request)
