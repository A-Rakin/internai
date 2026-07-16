from django.urls import path
from administration import views

app_name = 'administration'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('user-management/', views.user_management, name='user_management'),
    path('user-detail/<int:pk>/', views.user_detail, name='user_detail'),
    path('internship-moderation/', views.internship_moderation, name='internship_moderation'),
    path('company-management/', views.company_management, name='company_management'),
    path('activity-logs/', views.activity_logs, name='activity_logs'),
    path('platform-settings/', views.platform_settings, name='platform_settings'),
]
