# Mission 106 - Canary Deployment Router
# Fix the 2 bugs in this script.
import random

class CanaryRouter:
    def __init__(self, stable_url, canary_url, canary_pct=10):
        self.stable_url = stable_url
        self.canary_url = canary_url
        self.canary_pct = canary_pct  # BUG 1: should be clamped to [0, 100]

    def route(self):
        """Return the URL to route this request to."""
        r = random.randint(1, 100)
        if r > self.canary_pct:  # BUG 2: logic inverted — should be r <= canary_pct
            return self.canary_url
        return self.stable_url

    def set_canary_pct(self, pct):
        self.canary_pct = max(0, min(100, pct))
