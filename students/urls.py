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
]
