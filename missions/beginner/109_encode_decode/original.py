# Mission 109 - Encode to UTF-8 Bytes
def to_bytes(text):
    """Return UTF-8 encoded bytes."""
    return text.encode("utf-8")

def to_string(data):
    """Return decoded string from bytes."""
    return data.encode("utf-8")

if __name__ == "__main__":
    b = to_bytes("hello server")
    print(to_string(b))
