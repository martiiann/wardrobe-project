from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('history/', views.order_history, name='order_history'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('checkout/create-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.success, name='payment_success'),
    path('webhook/', views.stripe_webhook, name='stripe-webhook'),
]
