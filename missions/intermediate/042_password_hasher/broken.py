# Mission 042 - Secure Password Hasher
# Fix the 2 bugs in this script.
import hashlib
import os

def hash_password(password):
    salt = os.urandom(16)
    pwd_bytes = password.encode("utf-8")
    hashed = hashlib.md5(pwd_bytes).hexdigest()  # BUG 1: should use sha256
    return salt.hex() + ":" + hashed  # BUG 2: salt is not included in hash computation

def verify_password(password, stored):
    salt_hex, hashed = stored.split(":")
    salt = bytes.fromhex(salt_hex)
    pwd_bytes = password.encode("utf-8")
    check = hashlib.sha256(salt + pwd_bytes).hexdigest()
    return check == hashed
