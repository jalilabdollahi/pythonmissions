import pytest
import sys
sys.path.insert(0, ".")
from broken import validate_ssh_key, is_ed25519

VALID_KEY = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFAKE user@host"

def test_valid_key():
    ok, msg = validate_ssh_key(VALID_KEY)
    assert ok

def test_invalid_type():
    ok, msg = validate_ssh_key("ssh-dsa AAAAB user@host")
    assert not ok
    assert "Unknown key type" in msg

def test_is_ed25519():
    assert is_ed25519(VALID_KEY) is True

def test_is_not_rsa():
    rsa_key = "ssh-rsa AAAAB3NzaC user@host"
    assert is_ed25519(rsa_key) is False
