import pytest
import sys
sys.path.insert(0, ".")
from broken import hash_password, verify_password

def test_hash_format():
    result = hash_password("s3cr3t")
    assert ":" in result
    salt, hashed = result.split(":")
    assert len(salt) == 32  # 16 bytes = 32 hex chars

def test_verify_correct():
    stored = hash_password("mypassword")
    assert verify_password("mypassword", stored)

def test_verify_wrong():
    stored = hash_password("mypassword")
    assert not verify_password("wrongpassword", stored)

def test_not_md5():
    result = hash_password("test")
    _, hashed = result.split(":")
    assert len(hashed) == 64  # sha256 = 64 hex chars, md5 = 32
