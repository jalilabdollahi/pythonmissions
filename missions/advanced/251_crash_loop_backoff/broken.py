# Mission 251 - Worker Supervisor Restarts
# Restart policy for a process supervisor: backoff, stability reset, crash-loop detection.
from collections import namedtuple

Decision = namedtuple("Decision", ["action", "delay", "reason"])


class RestartPolicy:
    def __init__(self, mode="on-failure", base_delay=1.0, max_delay=30.0,
                 stable_after=60.0, max_crashes=5, window=120.0):
        if mode not in ("always", "on-failure", "never"):
            raise ValueError(f"unknown restart mode {mode!r}")
        self.mode = mode
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.stable_after = stable_after
        self.max_crashes = max_crashes
        self.window = window


class Supervised:
    """Tracks one child process; the caller reports starts and exits with timestamps."""

    def __init__(self, name, policy):
        self.name = name
        self.policy = policy
        self.started_at = None
        self.consecutive_failures = 0
        self.crash_times = []
        self.state = "stopped"

    def started(self, now):
        self.started_at = now
        self.state = "running"

    def _recent_crashes(self, now):
        self.crash_times = [t for t in self.crash_times if now - t <= self.policy.window]
        return len(self.crash_times)

    def exited(self, exit_code, now):
        policy = self.policy
        uptime = now - self.started_at if self.started_at is not None else 0.0
        self.state = "exited"
        if policy.mode == "never":
            return Decision("stop", 0.0, "policy never restarts")
        if exit_code == 0:
            return Decision("restart", 0.0, "always policy restarts clean exits")
        self.consecutive_failures += 1
        self.crash_times.append(now)
        if self._recent_crashes(now) >= policy.max_crashes:
            self.state = "failed"
            return Decision("give_up", 0.0, f"{policy.max_crashes} crashes within {policy.window}s")
        delay = policy.base_delay * 2 ** (self.consecutive_failures - 1)
        return Decision("restart", delay, f"crash #{self.consecutive_failures}")

    def describe(self):
        return {
            "name": self.name,
            "state": self.state,
            "failures": self.consecutive_failures,
            "recent_crashes": len(self.crash_times),
        }


def simulate(policy, runs, name="worker"):
    """runs is a list of (uptime_seconds, exit_code); returns the decisions made."""
    proc = Supervised(name, policy)
    now = 0.0
    decisions = []
    for uptime, code in runs:
        proc.started(now)
        now += uptime
        decision = proc.exited(code, now)
        decisions.append(decision)
        if decision.action != "restart":
            break
        now += decision.delay
    return decisions
