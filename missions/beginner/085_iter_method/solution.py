# Mission 085 - Solution
class ServerPool:
    def __init__(self, hosts):
        self._hosts = list(hosts)

    def __iter__(self):
        return iter(self._hosts)

if __name__ == "__main__":
    pool = ServerPool(["web-01", "web-02", "web-03"])
    for host in pool:
        print(host)
