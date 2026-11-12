# Mission 181 - Trust No Webhook (solution)
# Sign and verify incoming webhook bodies with HMAC-SHA256.
import hashlib
import hmac
import json


def _to_bytes(value):
    return value.encode("utf-8") if isinstance(value, str) else value


def sign(secret, body):
    digest = hmac.new(_to_bytes(secret), _to_bytes(body), hashlib.sha256).hexdigest()
    return "sha256=" + digest


def verify(secret, body, header):
    if not header:
        return False
    expected = sign(secret, body)
    return hmac.compare_digest(expected.encode("utf-8"), header.encode("utf-8"))


def parse_event(secret, body, header):
    if not verify(secret, body, header):
        raise PermissionError("bad signature")
    return json.loads(_to_bytes(body).decode("utf-8"))


def main():
    secret = "demo-secret"
    body = '{"event": "ping"}'
    header = sign(secret, body)
    print("header:", header)
    print("valid:", verify(secret, body, header))
    print("tampered:", verify(secret, body + " ", header))


if __name__ == "__main__":
    main()
