import pytest, sys
sys.path.insert(0, ".")
from broken import mask_secrets

def test_mask_password():
    text = "Connecting with password=supersecret123 to db"
    result = mask_secrets(text)
    assert "supersecret123" not in result
    assert "password=****" in result

def test_mask_bearer():
    text = "Authorization: Bearer eyJhbGciOiJSUzI1NiJ9.payload.sig"
    result = mask_secrets(text)
    assert "eyJhbGciOiJSUzI1NiJ9" not in result
    assert "Bearer ****" in result

def test_no_false_positive():
    text = "server started on port 8080"
    assert mask_secrets(text) == text
