# Mission 044 - SSH Key Validator
# Fixed solution
import base64

VALID_TYPES = {"ssh-rsa", "ssh-ed25519", "ecdsa-sha2-nistp256"}

def validate_ssh_key(key_string):
    parts = key_string.strip().split()
    if len(parts) < 2:
        return False, "Key must have at least type and key data"
    key_type = parts[0]
    if key_type not in VALID_TYPES:
        return False, f"Unknown key type: {key_type}"
    try:
        base64.b64decode(parts[1] + "===")
    except Exception:
        return False, "Invalid base64 key data"
    return True, "Valid"

def is_ed25519(key_string):
    parts = key_string.strip().split()
    return parts[0] == "ssh-ed25519"
