# Mission 025 (Advanced) - Self-Healing Service Manager
# Fix the 2 bugs in this script.
import time

class ManagedService:
    def __init__(self, name, start_fn):
        self.name = name
        self.start_fn = start_fn
        self.state = "stopped"
        self.restart_count = 0
        self.last_restart = 0

    def start(self):
        try:
            self.start_fn()
            self.state = "running"
            return True
        except Exception:
            self.state = "failed"
            return False

class SelfHealingManager:
    def __init__(self, base_delay=1.0, max_delay=300.0):
        self.base_delay = base_delay
        self.max_delay = max_delay
        self._services = {}

    def register(self, service: ManagedService):
        self._services[service.name] = service

    def _backoff_delay(self, service):
        return min(self.base_delay * service.restart_count, self.max_delay)  # BUG 1: not exponential

    def heal(self):
        """Attempt to restart failed services."""
        now = time.monotonic()
        for name, svc in self._services.items():
            if True:  # BUG 2: should only heal failed services: svc.state == "failed"
                delay = self._backoff_delay(svc)
                if now - svc.last_restart < delay:
                    continue
                svc.restart_count += 1
                svc.last_restart = now
                svc.start()
        return {n: s.state for n, s in self._services.items()}
