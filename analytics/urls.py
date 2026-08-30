from django.urls import path
from analytics import views

app_name = 'analytics'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('student/', views.student_analytics, name='student_analytics'),
    path('company/', views.company_analytics, name='company_analytics'),
    path('supervisor/', views.supervisor_analytics, name='supervisor_analytics'),
    path('admin/', views.admin_analytics, name='admin_analytics'),
]
