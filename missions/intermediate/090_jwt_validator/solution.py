# Mission 090 - JWT Validator
# Fixed solution
import time
import base64
import json
import hmac
import hashlib

def _b64url_decode(s):
    s += "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s)

def validate_jwt(token, secret):
    parts = token.split(".")
    if len(parts) != 3:
        return False, "Invalid token format"
    header_b64, payload_b64, sig_b64 = parts
    try:
        payload = json.loads(_b64url_decode(payload_b64))
    except Exception:
        return False, "Invalid payload"

    exp = payload.get("exp")
    if exp and time.time() > exp:
        return False, "Token expired"

    signing_input = f"{header_b64}.{payload_b64}"
    expected_sig = hmac.new(
        secret.encode(), signing_input.encode(), hashlib.sha256
    ).digest()

    actual_sig = _b64url_decode(sig_b64)
    if not hmac.compare_digest(expected_sig, actual_sig):
        return False, "Invalid signature"

    return True, payload
