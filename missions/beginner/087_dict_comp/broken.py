# Mission 087 - Build the Status Map
def status_map(servers):
    """Return {name: status} dict from server list."""
    return {s["status"]: s["name"] for s in servers}

if __name__ == "__main__":
    svrs = [{"name":"web-01","status":"healthy"},{"name":"web-02","status":"down"}]
    print(status_map(svrs))
