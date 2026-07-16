from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

def login_view(request):
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('landing:home')

def register_student(request):
    return render(request, 'accounts/register_student.html')

def register_company(request):
    return render(request, 'accounts/register_company.html')

def register_supervisor(request):
    return render(request, 'accounts/register_supervisor.html')

def forgot_password(request):
    return render(request, 'accounts/forgot_password.html')

def reset_password(request):
    return render(request, 'accounts/reset_password.html')

@login_required
def change_password(request):
    return render(request, 'accounts/change_password.html')

@login_required
def dashboard_redirect(request):
    return redirect(request.user.get_dashboard_url())
