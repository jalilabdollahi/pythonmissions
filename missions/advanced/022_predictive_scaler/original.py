# Mission 022 (Advanced) - Predictive Auto-Scaler
# Fix the 2 bugs in this script.

class PredictiveScaler:
    def __init__(self, min_replicas=1, max_replicas=20, threshold=0.8):
        self.min_replicas = min_replicas
        self.max_replicas = max_replicas
        self.threshold = threshold
        self.history = []

    def record(self, load):
        self.history.append(load)
        if len(self.history) > 60:
            self.history.pop(0)

    def forecast(self, steps_ahead=5):
        """Linear regression forecast."""
        if len(self.history) < 2:
            return self.history[-1] if self.history else 0.0
        n = len(self.history)
        xs = list(range(n))
        ys = self.history
        xm = sum(xs) / n
        ym = sum(ys) / n
        num = sum((x - xm) * (y - ym) for x, y in zip(xs, ys))
        den = sum((x - xm) ** 2 for x in xs)
        slope = num / den if den != 0 else 0
        intercept = ym - slope * xm
        return slope * (n - 1 + steps_ahead) + intercept  # correct

    def desired_replicas(self, current_replicas):
        forecast = self.forecast()
        current_load = self.history[-1] if self.history else 0
        if current_load > self.threshold:  # BUG 1: should use forecast not current_load
            target = int(current_replicas * (current_load / self.threshold)) + 1
        else:
            target = current_replicas - 1  # BUG 2: scale down by 1 is too aggressive — use max(min, cr-1)
        return max(self.min_replicas, min(self.max_replicas, target))
