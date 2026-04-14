# Mission 017 - Solution

def format_endpoint(host, port):
    return f"{host}:{port}"

if __name__ == "__main__":
    print(format_endpoint("web-01", 8080))
