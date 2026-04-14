# Mission 012 - Solution

def is_secure(url):
    return url.startswith("https://")

if __name__ == "__main__":
    print(is_secure("https://api.internal/health"))
    print(is_secure("http://api.internal/health"))
