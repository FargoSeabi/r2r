from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('checkout/<int:amount>/', views.payfast_checkout, name='payfast_checkout'),
    path('ticket/', views.ticket_form, name='ticket_form'),                 # shows the form
    path('payment-notify/', views.payfast_notify, name='payfast_notify'),  # PayFast server-to-server notify URL
    path('payment-return/', views.payfast_return, name='payfast_return'),  #
    path('payment-cancel/', views.payfast_cancel, name='payfast_cancel'),  #
    path("payment-success//", views.payment_success, name="payment_success"),
    path('zithulele/', views.zithulele, name='zithulele'),
    # path('ticket/checkout/', views.start_ticket_checkout, name='ticket_checkout'),  # server computes amount → renders PayFast post page
    # path('payment-success/', views.payment_success, name='payment_success'),
    # path('payment-cancel/', views.payment_cancel, name='payment_cancel'),
    # path('payment-notify/', views.payment_notify, name='payment_notify'),
]
