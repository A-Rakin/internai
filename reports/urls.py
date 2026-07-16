from django.urls import path
from reports import views

app_name = 'reports'

urlpatterns = [
    path('', views.list, name='list'),
    path('<int:pk>/', views.detail, name='detail'),
]
