# Mission 049 - Solution

def get_status(code):
    if code == 200:
        return "healthy"
    else:
        return "unhealthy"

if __name__ == "__main__":
    status = get_status(200)
    print(f"Status is: {status}")
