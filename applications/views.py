"""
============================================================
Applications Views - Application Submission & List
============================================================
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from accounts.decorators import role_required
from accounts.models import StudentProfile
from internships.models import Internship
from applications.models import Application
from notifications.models import Notification
from documents.models import ActivityLog


@login_required
@role_required('student')
def submit(request, internship_id=None):
    """Submit an application to an internship."""
    internship = get_object_or_404(Internship, pk=internship_id, is_approved=True, status='open')
    student_profile = get_object_or_404(StudentProfile, user=request.user)

    # Check if already applied
    if Application.objects.filter(student=student_profile, internship=internship).exists():
        messages.warning(request, 'You have already applied for this internship.')
        return redirect('internships:detail', pk=internship.pk)

    if request.method == 'POST':
        cover_letter = request.POST.get('cover_letter', '').strip()
        resume_file = request.FILES.get('resume')

        # Compute AI Match Score from uploaded PDF resume
        ai_score = 75
        if resume_file:
            try:
                from common.ai_engine import extract_text_from_pdf, calculate_skill_match
                resume_text = extract_text_from_pdf(resume_file)
                match_result = calculate_skill_match(resume_text, internship)
                ai_score = match_result['score']
            except Exception as e:
                print(f"AI Analysis Error: {e}")

        application = Application.objects.create(
            student=student_profile,
            internship=internship,
            cover_letter=cover_letter,
            resume=resume_file,
            status='pending',
            ai_match_score=ai_score,
        )

        # Log activity
        ActivityLog.objects.create(
            user=request.user,
            action='application_submit',
            description=f'Applied for "{internship.title}" at {internship.company.company_name}',
        )

        # Notify company
        Notification.objects.create(
            recipient=internship.company.user,
            notification_type='application',
            title=f'New Application: {internship.title}',
            message=f'{request.user.get_full_name()} submitted an application for {internship.title}.',
            link=f'/company/applicant-detail/{application.pk}/',
        )

        messages.success(request, 'Your application has been submitted successfully!')
        return redirect('students:applications')

    context = {'internship': internship}
    return render(request, 'applications/submit.html', context)


@login_required
def list(request):
    """Redirect to user role-specific applications view."""
    if request.user.is_student:
        return redirect('students:applications')
    elif request.user.is_company:
        return redirect('companies:applicants')
    else:
        messages.info(request, 'Applications list is role specific.')
        return redirect(request.user.get_dashboard_url())


@login_required
def detail(request, pk=None):
    """View application detail by pk."""
    if request.user.is_student:
        return redirect('students:application_detail', pk=pk)
    elif request.user.is_company:
        return redirect('companies:applicant_detail', pk=pk)
    else:
        return redirect(request.user.get_dashboard_url())


@login_required
@role_required('student')
def generate_cover_letter_view(request, internship_id=None):
    """AJAX endpoint to generate an AI cover letter for an internship."""
    from django.http import JsonResponse
    from common.ai_engine import generate_cover_letter

    internship = get_object_or_404(Internship, pk=internship_id)
    student_profile = get_object_or_404(StudentProfile, user=request.user)

    try:
        cover_letter = generate_cover_letter(student_profile, internship)
        return JsonResponse({'success': True, 'cover_letter': cover_letter})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

