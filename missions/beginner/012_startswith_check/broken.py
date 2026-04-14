# Mission 012 - Check the Protocol
# Fix the bug.

def is_secure(url):
    """Return True if the URL uses HTTPS."""
    return url.startswith("htps://")

if __name__ == "__main__":
    print(is_secure("https://api.internal/health"))
    print(is_secure("http://api.internal/health"))
