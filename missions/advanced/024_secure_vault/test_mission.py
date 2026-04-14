import pytest, sys
sys.path.insert(0, ".")
from broken import SecretsVault

def test_encrypt_decrypt():
    vault = SecretsVault("master-password-123")
    ct = vault.encrypt("supersecret")
    pt = vault.decrypt(ct)
    assert pt == "supersecret"

def test_unique_nonces():
    vault = SecretsVault("password")
    ct1 = vault.encrypt("same")
    ct2 = vault.encrypt("same")
    assert ct1[:12] != ct2[:12]  # different nonces each time

def test_kdf_iterations():
    import hashlib
    vault = SecretsVault("pass")
    # key length should be 32 bytes
    assert len(vault._key) == 32
