from django.urls import path
from students import views

app_name = 'students'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile-edit/<int:pk>/', views.profile_edit, name='profile_edit'),
    path('applications/', views.applications, name='applications'),
    path('application-detail/<int:pk>/', views.application_detail, name='application_detail'),
    path('interviews/', views.interviews, name='interviews'),
    path('reports/', views.reports, name='reports'),
    path('report-submit/', views.report_submit, name='report_submit'),
    path('settings/', views.settings, name='settings'),

    # AI Interview Preparation
    path('interview-prep/<int:pk>/', views.interview_prep, name='interview_prep'),
    path('interview-prep-grade/', views.interview_prep_grade, name='interview_prep_grade'),

    # Saved Internships (Bookmarks)
    path('saved/', views.saved_internships, name='saved_internships'),
    path('toggle-bookmark/', views.toggle_bookmark, name='toggle_bookmark'),

    # Application & Placement Actions
    path('withdraw-application/<int:pk>/', views.withdraw_application, name='withdraw_application'),
    path('update-supervisor/', views.update_supervisor, name='update_supervisor'),
]

