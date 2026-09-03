from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/student/', views.register_student, name='register_student'),
    path('register/company/', views.register_company, name='register_company'),
    path('register/supervisor/', views.register_supervisor, name='register_supervisor'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('change-password/', views.change_password, name='change_password'),
    path('suspended/', views.suspended_support, name='suspended'),
    path('redirect/', views.dashboard_redirect, name='dashboard_redirect'),
]
