from django.urls import path
from billing import views

app_name = 'billing'

urlpatterns = [
    path('create-checkout-session/<str:plan_name>/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.payment_success, name='success'),
    path('cancel/', views.payment_cancel, name='cancel'),
]
