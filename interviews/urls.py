from django.urls import path
from interviews import views

app_name = 'interviews'

urlpatterns = [
    path('', views.list, name='list'),
    path('<int:pk>/', views.detail, name='detail'),
]
