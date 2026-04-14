# Mission 094 - Round-Robin Load Balancer
# Fixed solution

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
        healthy = [s for s in self.servers if s["healthy"]]
        if not healthy:
            raise RuntimeError("No servers available")
        server = healthy[self._index % len(healthy)]
        self._index += 1
        return server["host"]
