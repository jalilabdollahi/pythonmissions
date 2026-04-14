# Mission 086 - Filter Healthy Servers
def healthy_servers(servers):
    """Return names of servers with status 'healthy'."""
    return [s["name"] if s["status"] == "healthy" for s in servers]

if __name__ == "__main__":
    svrs = [{"name":"web-01","status":"healthy"},{"name":"web-02","status":"down"},{"name":"web-03","status":"healthy"}]
    print(healthy_servers(svrs))
