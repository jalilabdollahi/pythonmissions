# Mission 019 (Advanced) - Chaos Engineering
# Fixed solution
import random
import time

class ChaosFramework:
    def __init__(self, services):
        self.services = list(services)
        self._failures = {}

    def inject_latency(self, service, latency_ms, duration_s):
        expiry = time.monotonic() + duration_s
        self._failures[service] = {"type": "latency", "ms": latency_ms, "expiry": expiry}

    def inject_failure(self, service, duration_s):
        expiry = time.monotonic() + duration_s
        self._failures[service] = {"type": "failure", "expiry": expiry}

    def blast_radius(self, fraction):
        count = int(len(self.services) * fraction)
        targets = random.sample(self.services, min(count, len(self.services)))
        for svc in targets:
            self.inject_failure(svc, duration_s=60)
        return targets

    def is_healthy(self, service):
        failure = self._failures.get(service)
        if failure is None:
            return True
        if time.monotonic() > failure["expiry"]:
            del self._failures[service]
            return True
        return False

    def active_failures(self):
        now = time.monotonic()
        return {s: f for s, f in self._failures.items() if now <= f["expiry"]}
