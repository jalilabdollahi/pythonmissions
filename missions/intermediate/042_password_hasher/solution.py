# Mission 042 - Secure Password Hasher
# Fixed solution
import hashlib
import os

def hash_password(password):
    salt = os.urandom(16)
    pwd_bytes = password.encode("utf-8")
    hashed = hashlib.sha256(salt + pwd_bytes).hexdigest()
    return salt.hex() + ":" + hashed

def verify_password(password, stored):
    salt_hex, hashed = stored.split(":")
    salt = bytes.fromhex(salt_hex)
    pwd_bytes = password.encode("utf-8")
    check = hashlib.sha256(salt + pwd_bytes).hexdigest()
    return check == hashed
