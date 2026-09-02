from django.urls import path
from documents import views

app_name = 'documents'

urlpatterns = [
    path('', views.list, name='list'),
    path('delete/<int:pk>/', views.delete_document, name='delete'),
]
