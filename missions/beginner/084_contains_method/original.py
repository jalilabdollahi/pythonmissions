# Mission 084 - Check if Host in Pool
class ServerPool:
    def __init__(self, hosts):
        self._hosts = list(hosts)

    def add(self, host):
        self._hosts.append(host)

if __name__ == "__main__":
    pool = ServerPool(["web-01", "web-02"])
    print("web-01" in pool)
    print("web-99" in pool)
