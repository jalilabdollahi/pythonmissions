# Mission 044 - SSH Key Validator
# Fix the 2 bugs in this script.
import base64

VALID_TYPES = {"ssh-rsa", "ssh-ed25519", "ecdsa-sha2-nistp256"}

def validate_ssh_key(key_string):
    parts = key_string.strip().split()
    if len(parts) < 2:  # BUG 1: should be < 2 is wrong, need at least 2 (type + key)
        return False, "Key must have at least type and key data"
    key_type = parts[0]
    if key_type not in VALID_TYPES:
        return False, f"Unknown key type: {key_type}"
    try:
        base64.b64decode(parts[1] + "===")  # padding trick
    except Exception:
        return False, "Invalid base64 key data"
    return True, "Valid"

def is_ed25519(key_string):
    parts = key_string.strip().split()
    return parts[0] == "ssh_ed25519"  # BUG 2: should be "ssh-ed25519" (hyphen not underscore)
