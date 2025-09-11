from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ticket-form/', views.ticket_form, name='ticket_form'),
    path('payfast-checkout/', views.payfast_checkout, name='payfast_checkout'),
    path('payfast/notify/', views.payfast_notify, name='payfast_notify'),
    path('payfast/return/', views.payfast_return, name='payfast_return'),
    path('payfast/cancel/', views.payfast_cancel, name='payfast_cancel'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('zithulele/', views.zithulele, name='zithulele'),
]
