# myapp/views.py
from decimal import Decimal
import hashlib
from uuid import uuid4
from urllib.parse import quote
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
import random
from django.contrib import messages
from .models import Order
from .payfast_utils import payfast_signature, ip_in_trusted, payfast_host

def index(request):
    return render(request, "index.html")
def zithulele(request):
    return render(request, "zithulele.html")

def ticket_form(request):
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


def payfast_checkout(request, amount):
    order_id = random.randint(10, 99)
    order, created = Order.objects.get_or_create(
        pk=order_id,
        defaults={
            "user_email": "freddiemanyate03@gmail.com",
            "amount": f"{Decimal(amount):.2f}",
            "status": "PENDING",
        }
    )

    # Build ITN endpoints
    notify_url = f"{settings.PAYFAST_NOTIFY_URL}/"
    return_url = f"{settings.PAYFAST_RETURN_URL}/"
    cancel_url = f"{settings.PAYFAST_CANCEL_URL}/"

    # Required fields per PayFast
    pf_params = {
        "merchant_id": settings.PAYFAST_MERCHANT_ID,
        "merchant_key": settings.PAYFAST_MERCHANT_KEY,
        "return_url": return_url,
        "cancel_url": cancel_url,
        "notify_url": notify_url,

        # Customer/order
        "name_first": "Customer",
        "name_last": "Order",
        "email_address": "freddiemanyate03@gmail.com",

        # Transaction
        "m_payment_id": str(order.id),       # your reference
        "amount": f"{amount:.2f}",     # must be string with 2 decimals
        "item_name": "Roots to Realities Booking",
        "item_description": f"Order {order.id}",
    }

    # signature = payfast_signature(pf_params, settings.PAYFAST_PASSPHRASE)
    # pf_params["signature"] = signature
    # print("PayFast signature:", signature)  # debug
    # Render an auto-submit form to POST to PayFast
    context = {
        "action": f"{payfast_host()}/eng/process",
        "fields": pf_params,
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
        order = m_payment_id
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
    elif payment_status == "failed":
        order.status = Order.Status.FAILED
    elif payment_status == "cancelled":
        order.status = Order.Status.CANCELLED
    else:
        # Treat anything else as pending
        order.status = Order.Status.PENDING

    order.pf_payment_id = pf_payment_id
    order.pf_signature = received_signature
    order.save(update_fields=["status", "pf_payment_id", "pf_signature"])

    # 8) Return 200 OK quickly; queue heavy work (emails, fulfilment) to Celery.
    return HttpResponse("OK")

def payfast_return(request):
    # Optional: display receipt; consider reloading order by id passed in "m_payment_id" if needed
    return render(request, "payments/return.html")

def payfast_cancel(request):
    return render(request, "payments/cancel.html")

def payfast_return(request):
    """
    The customer’s browser lands here after PayFast.
    We DO NOT trust this as proof of payment. We show status based on our DB,
    ideally using the order_id we stored in session pre-redirect.
    """
    order_id = request.session.get("last_order_id")
    if not order_id:
        messages.info(request, "We could not locate your recent order. If you completed payment, your receipt will be emailed shortly.")
        return render(request, "payments/return.html", {"order": None, "paid": False})

    order = get_object_or_404(Order, pk=order_id)
    paid = (order.status == Order.Status.PAID)

    # Optional: clear the session pointer so refreshes don’t loop
    try:
        del request.session["last_order_id"]
    except KeyError:
        pass

    context = {"order": order, "paid": paid}
    return render(request, "payments/return.html", context)


def payment_success(request):
    """
    Customer lands here after PayFast redirect.
    We check our DB (updated by ITN) to show the right message.
    """
    order_id = request.session.get("last_order_id")  # saved before redirect
    if not order_id:
        messages.info(request, "We could not find your recent order. If you completed payment, check your email for confirmation.")
        return render(request, "payments/payment_success.html", {"order": None, "paid": False})

    order = get_object_or_404(Order, pk=order_id)
    paid = (order.status == Order.Status.PAID)

    # Clear the session so refreshes don't reuse the ID
    request.session.pop("last_order_id", None)

    return render(request, "zithulele.html", {"order": order, "paid": paid})

# roots_to_realities/settings.py                                                                                                                                                                                                                                                                                                                                                                                                                                                            1