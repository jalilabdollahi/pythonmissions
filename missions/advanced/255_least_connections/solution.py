# Mission 255 - Least Connections Balancer (solution)
# Weighted least-connections routing with leases, draining and fair tie-breaking.


class NoCapacity(Exception):
    pass


class Server:
    def __init__(self, name, weight=1):
        if weight <= 0:
            raise ValueError("weight must be positive")
        self.name = name
        self.weight = weight
        self.active = 0
        self.draining = False
        self.last_pick = 0

    def load(self):
        return self.active / self.weight


class Lease:
    def __init__(self, server_name, lease_id):
        self.server = server_name
        self.id = lease_id
        self.released = False


class LeastConnections:
    def __init__(self, weights):
        self._servers = [Server(name, weight) for name, weight in weights.items()]
        self._tick = 0
        self._lease_ids = 0
        self.total_served = 0

    def _find(self, name):
        for server in self._servers:
            if server.name == name:
                return server
        raise KeyError(name)

    def acquire(self):
        candidates = [s for s in self._servers if not s.draining]
        if not candidates:
            raise NoCapacity("every server is draining")
        chosen = min(candidates, key=lambda s: (s.load(), s.last_pick))
        self._tick += 1
        self._lease_ids += 1
        chosen.last_pick = self._tick
        chosen.active += 1
        self.total_served += 1
        return Lease(chosen.name, self._lease_ids)

    def release(self, lease):
        if lease.released:
            return False
        lease.released = True
        server = self._find(lease.server)
        server.active -= 1
        return True

    def drain(self, name):
        self._find(name).draining = True

    def undrain(self, name):
        self._find(name).draining = False

    def remove(self, name):
        """Remove a server once it has no active connections."""
        server = self._find(name)
        if server.active > 0:
            return False
        self._servers.remove(server)
        return True

    def add(self, name, weight=1):
        self._servers.append(Server(name, weight))

    def snapshot(self):
        return {s.name: s.active for s in self._servers}

    def utilization(self):
        return {s.name: round(s.load(), 3) for s in self._servers}


def route_many(balancer, count):
    """Open `count` connections without closing any; return the chosen server names."""
    return [balancer.acquire().server for _ in range(count)]
