# Mission 082 - Secret Masker
# Fix the 2 bugs in this script.
import re

SECRET_PATTERNS = [
    r'(password|secret|token|api_key)=([^\s&]+)',
    r'Authorization: Bearer ([^\s]+)',
]

def mask_secrets(text):
    # Mask key=value style secrets
    text = re.sub(
        SECRET_PATTERNS[0],
        r'\2=****',  # BUG 1: should preserve key (\1) and mask value
        text,
        flags=re.IGNORECASE,
    )
    # Mask Bearer tokens
    text = re.sub(
        SECRET_PATTERNS[1],
        r'Authorization: Bearer \1',  # BUG 2: should mask \1 with ****
        text,
    )
    return text
