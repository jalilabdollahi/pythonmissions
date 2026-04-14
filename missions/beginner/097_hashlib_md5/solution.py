# Mission 097 - Solution
import hashlib

def hash_content(text):
    return hashlib.md5(text.encode()).hexdigest()

if __name__ == "__main__":
    cfg = "host=localhost\nport=5432\n"
    print(hash_content(cfg))
