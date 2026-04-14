# Mission 019 - Mask the Secret
# Fix the bug.

def mask_secret(s):
    """Return the secret with all but last 4 chars replaced by '*'."""
    return s[:-4] + "*" * 4

if __name__ == "__main__":
    print(mask_secret("mysupersecrettoken"))
