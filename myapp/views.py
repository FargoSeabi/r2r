# myapp/views.py
import hashlib
from uuid import uuid4
from urllib.parse import quote
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, "index.html")


def _pf_signature(data: dict, passphrase: str) -> str:
    """
    PayFast signing:
    1) Sort keys A→Z.
    2) URL-encode EACH value with percent-encoding (spaces => %20).
    3) Join as key=value&key=value...
    4) If passphrase is set, append &passphrase=... (also URL-encoded).
    5) MD5 the final string.
    """
    pairs = []
    for k in sorted(data.keys()):
        v = "" if data[k] is None else str(data[k]).strip()
        pairs.append(f"{k}={quote(v, safe='')}")                 # ✅ spaces -> %20
    payload = "&".join(pairs)
    if passphrase:
        payload = f"{payload}&passphrase={quote(passphrase.strip(), safe='')}"
    print("PF payload for signature:", payload)                  # debug
    sig = hashlib.md5(payload.encode("utf-8")).hexdigest()
    print("PF signature:", sig)                                  # debug
    return sig
@require_GET
@require_GET
def payfast_checkout(request):
    fields = {
        "merchant_id":   settings.PAYFAST_MERCHANT_ID.strip(),   # 10041623
        "merchant_key":  settings.PAYFAST_MERCHANT_KEY.strip(),  # 7busob28glxau
        "return_url":    settings.PAYFAST_RETURN_URL.strip(),
        "cancel_url":    settings.PAYFAST_CANCEL_URL.strip(),
        "notify_url":    settings.PAYFAST_NOTIFY_URL.strip(),
        "m_payment_id":  str(uuid4()),
        "amount":        "100.00",                                # 2 decimals
        "item_name":     "VR Village Experience",                 # ASCII
        "item_description": "Access to full 360 VR experience",
    }
    signature = _pf_signature(fields, settings.PAYFAST_PASSPHRASE)  # ikho.pass_2025_r2r
    return render(request, "checkout.html", {
        "payfast_url": settings.PAYFAST_PROCESS_URL,
        "fields": fields,
        "signature": signature,
    })


@require_GET
def payment_success(request):
    return HttpResponse("Payment successful! Thank you for your purchase.")


@require_GET
def payment_cancel(request):
    return HttpResponse("Payment cancelled. You have not been charged.")


@csrf_exempt
@require_POST
def payment_notify(request):
    # TODO: validate IPN signature & amounts later
    return HttpResponse("Notification received")
