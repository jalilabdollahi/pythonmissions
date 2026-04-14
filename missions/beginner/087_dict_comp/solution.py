# Mission 087 - Solution
def status_map(servers):
    return {s["name"]: s["status"] for s in servers}

if __name__ == "__main__":
    svrs = [{"name":"web-01","status":"healthy"},{"name":"web-02","status":"down"}]
    print(status_map(svrs))
