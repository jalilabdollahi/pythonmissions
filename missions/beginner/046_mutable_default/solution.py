# Mission 046 - Solution

def new_deployment(name, servers=None):
    if servers is None:
        servers = []
    return {"name": name, "servers": servers}

if __name__ == "__main__":
    d1 = new_deployment("prod")
    d1["servers"].append("web-01")
    d2 = new_deployment("staging")
    print(d2["servers"])
