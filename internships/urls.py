from django.urls import path
from internships import views

app_name = 'internships'

urlpatterns = [
    path('', views.browse, name='browse'),
    path('<int:pk>/', views.detail, name='detail'),
    path('search/', views.search_results, name='search_results'),
]
