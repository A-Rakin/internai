from django.urls import path
from messaging import views

app_name = 'messaging'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('thread/<int:pk>/', views.thread, name='thread'),
    path('compose/', views.compose, name='compose'),
]
