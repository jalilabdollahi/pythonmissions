# Mission 086 - Solution
def healthy_servers(servers):
    return [s["name"] for s in servers if s["status"] == "healthy"]

if __name__ == "__main__":
    svrs = [{"name":"web-01","status":"healthy"},{"name":"web-02","status":"down"},{"name":"web-03","status":"healthy"}]
    print(healthy_servers(svrs))
