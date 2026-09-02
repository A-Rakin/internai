from django.urls import path
from billing import views

app_name = 'billing'

urlpatterns = [
    # Demo Payment Gateway & Package Checkout
    path('checkout/<str:plan_code>/', views.checkout, name='checkout'),
    path('process-demo-payment/', views.process_demo_payment, name='process_demo_payment'),
    path('receipt/<str:transaction_id>/', views.receipt, name='receipt'),
    path('my-package/', views.my_package, name='my_package'),

    # Legacy routes
    path('create-checkout-session/<str:plan_name>/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.payment_success, name='success'),
    path('cancel/', views.payment_cancel, name='cancel'),
]
