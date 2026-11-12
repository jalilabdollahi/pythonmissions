# Mission 291 - Chaos Dial (solution)
# Seeded fault injector with per-target error rates and latency for resilience drills.
import random
from collections import Counter


class InjectedFault(Exception):
    pass


class Rule:
    def __init__(self, error_rate=0.0, latency_ms=0):
        if not 0.0 <= error_rate <= 1.0:
            raise ValueError("error_rate must be between 0 and 1")
        self.error_rate = error_rate
        self.latency_ms = latency_ms


class FaultInjector:
    """Wrap calls to named targets and fail or slow them down reproducibly."""

    def __init__(self, seed, rules, sleep):
        self.seed = seed
        self.rules = dict(rules)
        self.sleep = sleep
        self._rngs = {}
        self.injected = Counter()
        self.passed = Counter()

    def _rng(self, target):
        """One private random stream per target, derived from the experiment seed."""
        if target not in self._rngs:
            self._rngs[target] = random.Random(f"{self.seed}:{target}")
        return self._rngs[target]

    def call(self, target, fn, *args, **kwargs):
        rule = self.rules.get(target)
        if rule is None:
            return fn(*args, **kwargs)
        if rule.latency_ms:
            self.sleep(rule.latency_ms / 1000)
        if self._rng(target).random() < rule.error_rate:
            self.injected[target] += 1
            raise InjectedFault(f"chaos: {target} failed on purpose")
        self.passed[target] += 1
        return fn(*args, **kwargs)

    def wrap(self, target, fn):
        def wrapper(*args, **kwargs):
            return self.call(target, fn, *args, **kwargs)

        return wrapper

    def observed_rate(self, target):
        total = self.injected[target] + self.passed[target]
        return self.injected[target] / total if total else 0.0


def drill(injector, target, work, attempts):
    """Run `work` repeatedly and return the pattern of outcomes as a string of . and X."""
    pattern = []
    for _ in range(attempts):
        try:
            injector.call(target, work)
            pattern.append(".")
        except InjectedFault:
            pattern.append("X")
    return "".join(pattern)


def rules_from_spec(spec):
    """Build rules from a plain dict such as {"payments": {"error_rate": 0.2}}."""
    return {target: Rule(**options) for target, options in spec.items()}


if __name__ == "__main__":
    injector = FaultInjector(42, rules_from_spec({"search": {"error_rate": 0.3}}), lambda s: None)
    print(drill(injector, "search", lambda: None, 20))
