# Mission 085 - Iterate the Server Pool
class ServerPool:
    def __init__(self, hosts):
        self._hosts = list(hosts)

if __name__ == "__main__":
    pool = ServerPool(["web-01", "web-02", "web-03"])
    for host in pool:
        print(host)
