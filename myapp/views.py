# myapp/views.py
from decimal import Decimal
import hashlib
from uuid import uuid4
from urllib.parse import quote
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
import random
from django.contrib import messages
from django.utils import timezone
from .models import Order, Customer, Ticket
from .payfast_utils import payfast_signature, ip_in_trusted, payfast_host

def index(request):
    return render(request, "index.html")
def zithulele(request):
    return render(request, "zithulele.html")

def ticket_form(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        
        # Create or get customer
        customer, created = Customer.objects.get_or_create(
            email=email,
            defaults={
                'first_name': name,
                'last_name': surname,
                'phone': phone,
                'gender': gender,
                'age': int(age) if age else 18,
            }
        )
        
        # If customer exists but data is different, update it
        if not created:
            customer.first_name = name
            customer.last_name = surname
            customer.phone = phone
            customer.gender = gender
            customer.age = int(age) if age else 18
            customer.save()
        
        # Store customer ID in session for checkout
        request.session['customer_id'] = str(customer.id)
        request.session['customer_data'] = {
            'name': name,
            'surname': surname,
            'email': email,
            'phone': phone,
            'gender': gender,
            'age': age,
        }
        
        return redirect('payfast_checkout')
    
    return render(request, "ticket_form.html")

# def _pf_signature(data: dict, passphrase: str) -> str:
#     """
#     PayFast signing:
#     1) Sort keys A→Z.
#     2) URL-encode EACH value with percent-encoding (spaces => %20).
#     3) Join as key=value&key=value...
#     4) If passphrase is set, append &passphrase=... (also URL-encoded).
#     5) MD5 the final string.
#     """
#     pairs = []
#     for k in sorted(data.keys()):
#         v = "" if data[k] is None else str(data[k]).strip()
#         pairs.append(f"{k}={quote(v, safe='')}")                 # ✅ spaces -> %20
#     payload = "&".join(pairs)
#     if passphrase:
#         payload = f"{payload}&passphrase={quote(passphrase.strip(), safe='')}"
#     print("PF payload for signature:", payload)                  # debug
#     sig = hashlib.md5(payload.encode("utf-8")).hexdigest()
#     print("PF signature:", sig)                                  # debug
#     return sig
# @require_GET
# def payfast_checkout(request):
#     fields = {
#         "merchant_id":   settings.PAYFAST_MERCHANT_ID.strip(),   # 10041623
#         "merchant_key":  settings.PAYFAST_MERCHANT_KEY.strip(),  # 7busob28glxau
#         "return_url":    settings.PAYFAST_RETURN_URL.strip(),
#         "cancel_url":    settings.PAYFAST_CANCEL_URL.strip(),
#         "notify_url":    settings.PAYFAST_NOTIFY_URL.strip(),
#         "m_payment_id":  str(uuid4()),
#         "amount":        "100.00",                                # 2 decimals
#         "item_name":     "VR Village Experience",                 # ASCII
#         "item_description": "Access to full 360 VR experience",
#     }
#     # signature = _pf_signature(fields, settings.PAYFAST_PASSPHRASE)  # ikho.pass_2025_r2r
#     return render(request, "checkout.html", {
#         "payfast_url": settings.PAYFAST_PROCESS_URL,
#         "fields": fields,
#         # "signature": signature,
#     })


def payfast_checkout(request):
    # Get customer data from session
    customer_data = request.session.get('customer_data', {})
    customer_id = request.session.get('customer_id')
    
    if not customer_data or not customer_id:
        messages.error(request, 'Please fill out the ticket form first.')
        return redirect('ticket_form')
    
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        messages.error(request, 'Customer not found. Please fill out the form again.')
        return redirect('ticket_form')
    
    # Create ticket first
    ticket = Ticket.objects.create(
        customer=customer,
        ticket_type='standard',
        price=Decimal('35.00'),
        status='active'
    )
    
    # Create order and link to customer and ticket
    order = Order.objects.create(
        customer=customer,
        user_email=customer.email,
        amount=ticket.price,
        status='pending'
    )
    
    # Link ticket to order
    order.tickets.add(ticket)
    
    # Build ITN endpoints
    notify_url = settings.PAYFAST_NOTIFY_URL
    return_url = settings.PAYFAST_RETURN_URL
    cancel_url = settings.PAYFAST_CANCEL_URL

    # Required fields per PayFast
    pf_params = {
        "merchant_id": settings.PAYFAST_MERCHANT_ID,
        "merchant_key": settings.PAYFAST_MERCHANT_KEY,
        "return_url": return_url,
        "cancel_url": cancel_url,
        "notify_url": notify_url,

        # Customer/order
        "name_first": customer.first_name,
        "name_last": customer.last_name,
        "email_address": customer.email,
        "cell_number": customer.phone,

        # Transaction
        "m_payment_id": str(order.id),       # your reference
        "amount": str(order.amount),     # must be string with 2 decimals
        "item_name": "VR Experience Ticket",
        "item_description": "Virtual Reality Experience at Ikho",
    }

    # Generate signature
    signature = payfast_signature(pf_params, settings.PAYFAST_PASSPHRASE)
    pf_params["signature"] = signature
    
    # Store order and ticket IDs in session
    request.session['order_id'] = str(order.id)
    request.session['ticket_id'] = str(ticket.id)
    
    # Render an auto-submit form to POST to PayFast
    context = {
        "action": f"{payfast_host()}/eng/process",
        "fields": pf_params,
        "customer": customer,
        "order": order,
        "ticket": ticket,
    }
    return render(request, "payments/payfast_redirect.html", context)


@csrf_exempt
@require_POST
def payfast_notify(request):
    print("PayFast notify POST data:", request.POST)  # debug
    # 1) Basic IP allowlist (optional but recommended)
    source_ip = request.META.get("REMOTE_ADDR", "")
    if not ip_in_trusted(source_ip):
        return HttpResponseBadRequest("Untrusted source IP")

    # 2) Parse POST data as dict[str, str]
    posted = {k: v for k, v in request.POST.items()}
    received_signature = posted.get("signature", "")
    print("PayFast notify signature:", received_signature)  # debug
    if not received_signature:
        return HttpResponseBadRequest("Missing signature")

    # 3) Verify signature (recompute from posted params EXCLUDING 'signature')
    verify_params = {k: v for k, v in posted.items() if k != "signature"}
    calc_sig = payfast_signature(verify_params, settings.PAYFAST_PASSPHRASE)
    if calc_sig != received_signature:
        return HttpResponseBadRequest("Bad signature")

    # 4) Validate merchant id
    if posted.get("merchant_id") != settings.PAYFAST_MERCHANT_ID:
        return HttpResponseBadRequest("Bad merchant_id")

    # 5) Load the order and validate amount
    m_payment_id = posted.get("m_payment_id")
    pf_payment_id = posted.get("pf_payment_id", "")
    amount_gross = posted.get("amount_gross") or posted.get("amount")
    if not (m_payment_id and amount_gross):
        return HttpResponseBadRequest("Missing order or amount")

    try:
        order = Order.objects.get(id=m_payment_id)
    except Order.DoesNotExist:
        return HttpResponseBadRequest("Order not found")

    try:
        amount_gross = Decimal(amount_gross)
    except Exception:
        return HttpResponseBadRequest("Invalid amount")

    if amount_gross != order.amount:
        # Defensive: you may allow slight rounding deltas if needed
        return HttpResponseBadRequest("Amount mismatch")

    # 6) Optional: Validate that PayFast can reach back to your notify_url (validation step)
    # Historically PayFast provided a validation POST-back; if you implement it, do it here.

    # 7) Interpret payment status
    payment_status = posted.get("payment_status", "").lower()
    # Common statuses: "COMPLETE", "FAILED", "PENDING"
    if payment_status == "complete":
        order.status = Order.Status.PAID
        order.paid_at = timezone.now()
        
        # Update all associated tickets to active status
        for ticket in order.tickets.all():
            ticket.status = 'active'
            ticket.save()
            
    elif payment_status == "failed":
        order.status = Order.Status.FAILED
        
        # Update all associated tickets to cancelled status
        for ticket in order.tickets.all():
            ticket.status = 'cancelled'
            ticket.save()
            
    elif payment_status == "cancelled":
        order.status = Order.Status.CANCELLED
        
        # Update all associated tickets to cancelled status
        for ticket in order.tickets.all():
            ticket.status = 'cancelled'
            ticket.save()
    else:
        # Treat anything else as pending
        order.status = Order.Status.PENDING

    order.pf_payment_id = pf_payment_id
    order.pf_signature = received_signature
    order.save(update_fields=["status", "pf_payment_id", "pf_signature", "paid_at"])

    # 8) Return 200 OK quickly; queue heavy work (emails, fulfilment) to Celery.
    return HttpResponse("OK")

def payfast_cancel(request):
    return render(request, "payments/cancel.html")

def payfast_return(request):
    """
    The customer's browser lands here after PayFast.
    We DO NOT trust this as proof of payment. We show status based on our DB,
    ideally using the order_id we stored in session pre-redirect.
    """
    # Get order ID from session or URL parameters
    order_id = request.session.get('order_id') or request.GET.get('m_payment_id')
    
    if not order_id:
        messages.error(request, 'No order found.')
        return redirect('ticket_form')
    
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        messages.error(request, 'Order not found.')
        return redirect('ticket_form')
    
    # Get customer and tickets
    customer = order.customer
    tickets = order.tickets.all()
    
    # Check order status
    if order.status == Order.Status.PAID:
        messages.success(request, f'Payment successful! Your VR experience ticket has been confirmed for {customer.first_name} {customer.last_name}.')
        # Store order info in session for payment success page
        request.session['successful_order_id'] = str(order.id)
        return redirect('payment_success')
    elif order.status == Order.Status.FAILED:
        messages.error(request, 'Payment failed. Please try again.')
        return redirect('ticket_form')
    elif order.status == Order.Status.CANCELLED:
        messages.warning(request, 'Payment was cancelled.')
        return redirect('ticket_form')
    else:
        messages.info(request, 'Payment is being processed. Please wait for confirmation.')
        # Store order info in session for payment success page
        request.session['pending_order_id'] = str(order.id)
        return redirect('payment_success')
    
    return redirect('ticket_form')


def payment_success(request):
    # Get order from session (either successful or pending)
    order_id = request.session.get('successful_order_id') or request.session.get('pending_order_id')
    
    if not order_id:
        messages.error(request, 'No order found.')
        return redirect('ticket_form')
    
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        messages.error(request, 'Order not found.')
        return redirect('ticket_form')
    
    # Get customer and tickets from database
    customer = order.customer
    tickets = order.tickets.all()
    
    # Quick verification: If payment is confirmed, redirect to Zithulele after short display
    auto_redirect = order.status == Order.Status.PAID
    
    context = {
        'order': order,
        'customer': customer,
        'tickets': tickets,
        'is_paid': order.status == Order.Status.PAID,
        'is_pending': order.status == Order.Status.PENDING,
        'auto_redirect': auto_redirect,  # Flag for auto-redirect
        'redirect_delay': 3000,  # 3 seconds delay for user to see confirmation
    }
    
    # Clear session data after displaying success page
    session_keys_to_clear = ['successful_order_id', 'pending_order_id', 'order_id', 'customer_id', 'ticket_id', 'customer_data']
    for key in session_keys_to_clear:
        if key in request.session:
            del request.session[key]
    
    return render(request, 'payments/payment_success.html', context)

# roots_to_realities/settings.py                                                                                                                                                                                                                                                                                                                                                                                                                                                            1