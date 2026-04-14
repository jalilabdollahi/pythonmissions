# Mission 094 - Round-Robin Load Balancer
# Fix the 2 bugs in this script.

class RoundRobinLB:
    def __init__(self, servers):
        self.servers = [{"host": s, "healthy": True} for s in servers]
        self._index = 0

    def mark_unhealthy(self, host):
        for s in self.servers:
            if s["host"] == host:
                s["healthy"] = False

    def mark_healthy(self, host):
        for s in self.servers:
            if s["host"] == host:
                s["healthy"] = True

    def next_server(self):
        all_servers = self.servers  # BUG 1: should only use healthy servers
        if not all_servers:
            raise RuntimeError("No servers available")
        server = all_servers[self._index]
        self._index += 1  # BUG 2: must wrap with modulo
        return server["host"]
