# Mission 097 - Hash the Config File
import hashlib

def hash_content(text):
    """Return MD5 hex digest of text."""
    return hashlib.md5(text).hexdigest()

if __name__ == "__main__":
    cfg = "host=localhost\nport=5432\n"
    print(hash_content(cfg))
