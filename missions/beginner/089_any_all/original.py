# Mission 089 - Check All Services Up
def all_healthy(services):
    """Return True only if every service status is 'up'."""
    return any(s["status"] == "up" for s in services)

if __name__ == "__main__":
    svcs = [{"name":"web","status":"up"},{"name":"db","status":"down"}]
    print(all_healthy(svcs))
