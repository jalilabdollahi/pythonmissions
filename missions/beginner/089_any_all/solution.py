# Mission 089 - Solution
def all_healthy(services):
    return all(s["status"] == "up" for s in services)

if __name__ == "__main__":
    svcs = [{"name":"web","status":"up"},{"name":"db","status":"down"}]
    print(all_healthy(svcs))
