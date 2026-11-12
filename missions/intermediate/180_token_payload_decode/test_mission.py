import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


import base64
import json


def b64url(raw):
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def make_token(claims):
    body = json.dumps(claims, ensure_ascii=False).encode("utf-8")
    return ".".join([b64url(b'{"alg":"none"}'), b64url(body), "sig"])


def test_decodes_segments_whatever_their_length():
    for n in range(1, 9):
        raw = bytes(range(65, 65 + n))
        assert broken.decode_segment(b64url(raw)) == raw, "length %d needs padding restored" % n


def test_url_safe_alphabet_is_respected():
    assert b64url(b"\xfb\xff\xfe") == "-__-"
    assert broken.decode_segment("-__-") == b"\xfb\xff\xfe", "'-' and '_' belong to the URL-safe alphabet"


def test_payload_with_unicode_and_symbols():
    claims = {"user": "zoë>>~"}
    assert broken.read_payload(make_token(claims)) == claims


def test_malformed_token_is_rejected():
    with pytest.raises(ValueError) as info:
        broken.read_payload("only.two")
    assert "malformed" in str(info.value)


def test_not_expired_before_exp():
    assert broken.is_expired(make_token({"exp": 1000}), now=999) is False


def test_expired_exactly_at_exp():
    assert broken.is_expired(make_token({"exp": 1000}), now=1000) is True


def test_token_without_exp_never_expires():
    assert broken.is_expired(make_token({"user": "x"}), now=10**12) is False


def test_describe():
    assert broken.describe(make_token({"user": "ana", "scope": "read"})) == "ana (read)"
    assert broken.describe(make_token({})) == "? (no scope)"
