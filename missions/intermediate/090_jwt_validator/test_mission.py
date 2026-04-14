import pytest, sys, time, json, base64, hmac, hashlib
sys.path.insert(0, ".")
from broken import validate_jwt, _b64url_decode

SECRET = "supersecret"

def make_token(payload, secret=SECRET):
    header = base64.urlsafe_b64encode(b'{"alg":"HS256"}').rstrip(b"=").decode()
    payload_b = base64.urlsafe_b64encode(json.dumps(payload).encode()).rstrip(b"=").decode()
    signing = f"{header}.{payload_b}"
    sig = hmac.new(secret.encode(), signing.encode(), hashlib.sha256).digest()
    sig_b64 = base64.urlsafe_b64encode(sig).rstrip(b"=").decode()
    return f"{header}.{payload_b}.{sig_b64}"

def test_valid_token():
    token = make_token({"sub": "user-1", "exp": int(time.time()) + 3600})
    ok, result = validate_jwt(token, SECRET)
    assert ok

def test_expired_token():
    token = make_token({"sub": "user-1", "exp": int(time.time()) - 1})
    ok, msg = validate_jwt(token, SECRET)
    assert not ok
    assert "expired" in msg

def test_wrong_secret():
    token = make_token({"sub": "user-1", "exp": int(time.time()) + 3600})
    ok, msg = validate_jwt(token, "wrongsecret")
    assert not ok
