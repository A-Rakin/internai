from django.urls import path
from chatbot import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chat_page, name='chat'),
    path('send/', views.send_message, name='send'),
    path('session/<int:pk>/', views.get_session, name='session'),
    path('session/<int:pk>/delete/', views.delete_session, name='delete_session'),
    path('new-session/', views.new_session, name='new_session'),
]
