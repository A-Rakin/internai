from django.urls import path
from companies import views

app_name = 'companies'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile-edit/<int:pk>/', views.profile_edit, name='profile_edit'),
    path('internship-create/', views.internship_create, name='internship_create'),
    path('internship-edit/<int:pk>/', views.internship_edit, name='internship_edit'),
    path('internship-list/', views.internship_list, name='internship_list'),
    path('applicants/', views.applicants, name='applicants'),
    path('applicant-detail/<int:pk>/', views.applicant_detail, name='applicant_detail'),
    path('interviews/', views.interviews, name='interviews'),
    path('interview-schedule/<int:pk>/', views.interview_schedule, name='interview_schedule'),
    path('ai-resume-analysis/', views.ai_resume_analysis, name='ai_resume_analysis'),
    path('ai-candidate-ranking/', views.ai_candidate_ranking, name='ai_candidate_ranking'),
    path('settings/', views.settings, name='settings'),
]
