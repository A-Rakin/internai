from django.urls import path
from supervisors import views

app_name = 'supervisors'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('students-list/', views.students_list, name='students_list'),
    path('student-detail/<int:pk>/', views.student_detail, name='student_detail'),
    path('report-review/', views.report_review, name='report_review'),
    path('evaluation/', views.evaluation, name='evaluation'),
    path('settings/', views.settings, name='settings'),
]
