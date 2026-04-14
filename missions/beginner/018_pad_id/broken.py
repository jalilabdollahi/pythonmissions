# Mission 018 - Pad the Task ID
# Fix the bug.

def pad_id(n):
    """Return n as a zero-padded 6-digit string."""
    return str(n).zfill(0)

if __name__ == "__main__":
    print(pad_id(42))
    print(pad_id(999999))
