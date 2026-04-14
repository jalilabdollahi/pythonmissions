# Mission 084 - Solution
class ServerPool:
    def __init__(self, hosts):
        self._hosts = list(hosts)

    def add(self, host):
        self._hosts.append(host)

    def __contains__(self, item):
        return item in self._hosts

if __name__ == "__main__":
    pool = ServerPool(["web-01", "web-02"])
    print("web-01" in pool)
    print("web-99" in pool)
