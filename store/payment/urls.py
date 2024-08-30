from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart, name='cart_path'),
    path('to/cart/<int:product_id>/<str:action>/', views.to_cart, name='to_cart_activate'),
    path('clear/cart/', views.clear_cart, name='clear_cart_activate'),
    path('checkout/', views.checkout, name='checkout_activate'),
    path('payment/', views.create_checkout_session, name='payment_path'),
    path('success/', views.success_payment, name='success_path')
]