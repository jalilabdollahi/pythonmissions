# Mission 024 (Advanced) - Secure Vault
# Fixed solution
import os
import hashlib

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

class SecretsVault:
    def __init__(self, master_password: str, salt: bytes = None):
        self.salt = salt or os.urandom(16)
        self._key = self._derive_key(master_password)

    def _derive_key(self, password: str) -> bytes:
        if not HAS_CRYPTO:
            return hashlib.pbkdf2_hmac("sha256", password.encode(), self.salt, 100000)
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=self.salt, iterations=100000)
        return kdf.derive(password.encode())

    def encrypt(self, plaintext: str) -> bytes:
        data = plaintext.encode()
        nonce = os.urandom(12)  # fresh nonce per encryption
        if HAS_CRYPTO:
            aesgcm = AESGCM(self._key)
            return nonce + aesgcm.encrypt(nonce, data, None)
        return nonce + data  # stub

    def decrypt(self, ciphertext: bytes) -> str:
        if HAS_CRYPTO:
            nonce = ciphertext[:12]
            aesgcm = AESGCM(self._key)
            return aesgcm.decrypt(nonce, ciphertext[12:], None).decode()
        return ciphertext[12:].decode()  # stub
