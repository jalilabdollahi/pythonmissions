# Mission 106 - Canary Deployment Router
# Fixed solution
import random

class CanaryRouter:
    def __init__(self, stable_url, canary_url, canary_pct=10):
        self.stable_url = stable_url
        self.canary_url = canary_url
        self.canary_pct = max(0, min(100, canary_pct))

    def route(self):
        r = random.randint(1, 100)
        if r <= self.canary_pct:
            return self.canary_url
        return self.stable_url

    def set_canary_pct(self, pct):
        self.canary_pct = max(0, min(100, pct))
