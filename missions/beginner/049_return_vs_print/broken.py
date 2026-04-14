# Mission 049 - Return the Status
# Fix the bug.

def get_status(code):
    """Return 'healthy' if code is 200, else 'unhealthy'."""
    if code == 200:
        print("healthy")
    else:
        print("unhealthy")

if __name__ == "__main__":
    status = get_status(200)
    print(f"Status is: {status}")
