import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


import hashlib
import hmac

BODY = b'{"event": "invoice.paid", "id": 7}'


def reference(secret, body):
    return "sha256=" + hmac.new(secret, body, hashlib.sha256).hexdigest()


def test_sign_matches_reference_for_bytes():
    assert broken.sign(b"k", BODY) == reference(b"k", BODY)


def test_str_secret_and_str_body_are_accepted():
    assert broken.sign("k", BODY.decode()) == reference(b"k", BODY), "HMAC needs bytes: encode str inputs"


def test_valid_signature_verifies():
    header = reference(b"k", BODY)
    assert broken.verify("k", BODY, header) is True


def test_wrong_signature_or_body_fails():
    header = reference(b"k", BODY)
    assert broken.verify("k", BODY + b" ", header) is False
    assert broken.verify("other", BODY, header) is False
    assert broken.verify("k", BODY, "sha256=deadbeef") is False


def test_missing_header_is_false_not_an_exception():
    assert broken.verify("k", BODY, None) is False
    assert broken.verify("k", BODY, "") is False


def test_comparison_is_constant_time(monkeypatch):
    calls = []
    real = hmac.compare_digest

    def spy(a, b):
        calls.append((a, b))
        return real(a, b)

    monkeypatch.setattr(broken.hmac, "compare_digest", spy)
    assert broken.verify("k", BODY, reference(b"k", BODY))
    assert calls, "use hmac.compare_digest instead of == to avoid timing leaks"


def test_parse_event_returns_json_for_good_signature():
    event = broken.parse_event("k", BODY, reference(b"k", BODY))
    assert event == {"event": "invoice.paid", "id": 7}


def test_parse_event_rejects_bad_signature():
    with pytest.raises(PermissionError) as info:
        broken.parse_event("k", BODY, "sha256=00")
    assert "bad signature" in str(info.value)
