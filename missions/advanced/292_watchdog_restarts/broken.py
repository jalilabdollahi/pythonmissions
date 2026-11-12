# Mission 292 - Watchdog Restarts
# Health watchdog: restart a service after N consecutive failures, but not in a storm.


class Watchdog:
    def __init__(self, check, restart, clock, threshold=3, cooldown=300):
        self.check = check
        self.restart = restart
        self.clock = clock
        self.threshold = threshold
        self.cooldown = cooldown
        self.consecutive = 0
        self.last_restart = 0
        self.restarts = 0
        self.restart_errors = []
        self.restart_times = []

    def tick(self):
        """Probe once. Returns healthy, degraded, cooling_down, restarted or restart_failed."""
        now = self.clock()
        if self.check():
            return "healthy"
        self.consecutive += 1
        if self.consecutive < self.threshold:
            return "degraded"
        if self.last_restart is not None and now - self.last_restart < self.cooldown:
            return "cooling_down"
        self.last_restart = now
        self.restart_times.append(now)
        self.restart()
        self.restarts += 1
        return "restarted"

    def is_flapping(self, window=3600, limit=3):
        """True when the service needed `limit` or more restart attempts inside the window."""
        recent = [t for t in self.restart_times if self.clock() - t <= window]
        return len(recent) >= limit

    def status(self):
        return {
            "consecutive_failures": self.consecutive,
            "restarts": self.restarts,
            "last_restart": self.last_restart,
            "flapping": self.is_flapping(),
            "restart_errors": list(self.restart_errors),
        }


def run_probes(watchdog, clock_state, count, interval=30):
    """Drive the watchdog `count` times, advancing a fake clock by `interval` each time."""
    outcomes = []
    for _ in range(count):
        outcomes.append(watchdog.tick())
        clock_state["now"] += interval
    return outcomes


if __name__ == "__main__":
    state = {"now": 0}
    dog = Watchdog(lambda: False, lambda: print("restarting daemon"), lambda: state["now"])
    print(run_probes(dog, state, 8))
    print(dog.status())
