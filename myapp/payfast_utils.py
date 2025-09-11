# payfast_utils.py
import hashlib, ipaddress, urllib.parse
from django.conf import settings

def payfast_host():
    return "https://sandbox.payfast.co.za" 
# if settings.PAYFAST_MODE == "sandbox" else "https://www.payfast.co.za"

def pf_normalize(params: dict) -> list[tuple[str, str]]:
    """Sort keys ASC, drop empty values, coerce to str, strip spaces."""
    items = []
    for k, v in params.items():
        if v is None:
            continue
        s = str(v).strip()
        if s == "":
            continue
        items.append((k, s))
    items.sort(key=lambda kv: kv[0])
    return items

def pf_query_string(params: dict, passphrase: str | None) -> str:
    """
    Build the exact string that PayFast expects you to hash:
    key=value&key=value ... with values percent-encoded, no spaces.
    If passphrase is set in your merchant settings, append &passphrase=... last.
    """
    parts = []
    for k, v in pf_normalize(params):
        # Encode each value; keys are ASCII, values must be percent-encoded
        # Use quote_plus to encode spaces as '+' and ensure hex encoding is uppercase
        encoded_value = urllib.parse.quote_plus(v, safe='')
        # Convert only hex encoding to uppercase (e.g., %3a -> %3A)
        encoded_value = ''.join(c.upper() if i > 0 and encoded_value[i-1] == '%' and c in '0123456789abcdef' else c 
                               for i, c in enumerate(encoded_value))
        parts.append(f"{k}={encoded_value}")
    q = "&".join(parts)
    if passphrase:
        encoded_passphrase = urllib.parse.quote_plus(passphrase, safe='')
        # Convert only hex encoding to uppercase
        encoded_passphrase = ''.join(c.upper() if i > 0 and encoded_passphrase[i-1] == '%' and c in '0123456789abcdef' else c 
                                    for i, c in enumerate(encoded_passphrase))
        q = f"{q}&passphrase={encoded_passphrase}"
    return q

def payfast_signature(params: dict, passphrase: str | None) -> str:
    q = pf_query_string(params, passphrase)
    return hashlib.md5(q.encode("utf-8")).hexdigest()

# def payfast_signature(params: dict, passphrase: str | None) -> str:
#     items = _normalize(params)
#     q = "&".join(f"{k}={urllib.parse.quote(v, safe='')}" for k, v in items)
#     if passphrase:
#         q = f"{q}&passphrase={urllib.parse.quote(passphrase, safe='')}"
#     return hashlib.md5(q.encode("utf-8")).hexdigest()

def ip_in_trusted(ip: str) -> bool:
    """Allow exact IPs and CIDR ranges in settings.PAYFAST_TRUSTED_IPS."""
    if not settings.PAYFAST_TRUSTED_IPS:
        return True  # if you choose to disable IP checking
    try:
        ip_obj = ipaddress.ip_address(ip)
    except ValueError:
        return False
    for net in settings.PAYFAST_TRUSTED_IPS:
        if "/" in net:
            if ip_obj in ipaddress.ip_network(net, strict=False):
                return True
        else:
            if ip == net:
                return True
    return False
