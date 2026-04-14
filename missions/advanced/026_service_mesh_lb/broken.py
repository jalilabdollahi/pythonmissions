# Mission 026 (Advanced) - Service Mesh Load Balancer
# Fix the 2 bugs in this script.
import random

class WeightedLoadBalancer:
    def __init__(self):
        self._endpoints = []  # {host, port, weight, healthy}

    def register(self, host, port, weight=1):
        self._endpoints.append({"host": host, "port": port, "weight": weight, "healthy": True})

    def mark_health(self, host, port, healthy):
        for ep in self._endpoints:
            if ep["host"] == host and ep["port"] == port:
                ep["healthy"] = healthy

    def select(self):
        pool = [ep for ep in self._endpoints]  # BUG 1: should only include healthy endpoints
        if not pool:
            raise RuntimeError("No endpoints available")
        total_weight = sum(ep["weight"] for ep in pool)
        r = random.uniform(0, total_weight)
        cumulative = 0
        for ep in pool:
            cumulative += ep["weight"]
            if r < cumulative:  # BUG 2: should be r <= cumulative for proper weighted selection
                return ep
        return pool[-1]
