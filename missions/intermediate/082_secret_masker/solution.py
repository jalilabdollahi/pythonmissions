# Mission 082 - Secret Masker
# Fixed solution
import re

SECRET_PATTERNS = [
    r'(password|secret|token|api_key)=([^\s&]+)',
    r'Authorization: Bearer ([^\s]+)',
]

def mask_secrets(text):
    text = re.sub(
        SECRET_PATTERNS[0],
        r'\1=****',
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        SECRET_PATTERNS[1],
        r'Authorization: Bearer ****',
        text,
    )
    return text
