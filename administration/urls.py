from django.urls import path
from administration import views

app_name = 'administration'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('user-management/', views.user_management, name='user_management'),
    path('user-detail/<int:pk>/', views.user_detail, name='user_detail'),
    path('user-cancel-subscription/<int:pk>/', views.user_cancel_subscription, name='user_cancel_subscription'),
    path('user-suspend/<int:pk>/', views.user_suspend, name='user_suspend'),
    path('user-delete/<int:pk>/', views.user_delete, name='user_delete'),
    path('internship-moderation/', views.internship_moderation, name='internship_moderation'),
    path('internship-preview/<int:pk>/', views.internship_preview, name='internship_preview'),
    path('internship-edit/<int:pk>/', views.admin_internship_edit, name='internship_edit'),
    path('internship-unpublish/<int:pk>/', views.internship_unpublish, name='internship_unpublish'),
    path('company-management/', views.company_management, name='company_management'),
    path('activity-logs/', views.activity_logs, name='activity_logs'),
    path('platform-settings/', views.platform_settings, name='platform_settings'),
]
