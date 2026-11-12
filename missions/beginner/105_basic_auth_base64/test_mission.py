import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import basic_auth_header, read_basic_auth, registry_headers


def test_known_header_value():
    assert basic_auth_header("ci-bot", "s3cret") == "Basic Y2ktYm90OnMzY3JldA=="


def test_header_is_a_str():
    assert isinstance(basic_auth_header("a", "b"), str), "decode the base64 bytes before joining them to text"


def test_roundtrip_with_non_ascii_password():
    header = basic_auth_header("deploy", "pässwörd")
    assert read_basic_auth(header) == ("deploy", "pässwörd")


def test_password_may_contain_colon():
    assert read_basic_auth(basic_auth_header("u", "a:b:c")) == ("u", "a:b:c")


def test_wrong_scheme_is_rejected():
    with pytest.raises(ValueError):
        read_basic_auth("Bearer abc123")


def test_registry_headers_contains_authorization():
    assert registry_headers("a", "b")["Authorization"].startswith("Basic ")
