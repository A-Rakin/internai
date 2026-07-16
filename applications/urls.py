from django.urls import path
from applications import views

app_name = 'applications'

urlpatterns = [
    path('submit/<int:internship_id>/', views.submit, name='submit'),
    path('', views.list, name='list'),
    path('<int:pk>/', views.detail, name='detail'),
]
