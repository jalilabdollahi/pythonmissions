# Mission 260 - Pod Autoscaler Math (solution)
# Horizontal-pod-autoscaler style replica calculation with tolerance, bounds and scale-down stabilization.
import math
from collections import namedtuple

Metric = namedtuple("Metric", ["name", "value", "target"])


def metric_proposal(current, metric, tolerance):
    """Replicas this single metric asks for, or None if it has no data."""
    if metric.value is None:
        return None
    if metric.target <= 0:
        raise ValueError(f"target for {metric.name} must be positive")
    ratio = metric.value / metric.target
    if round(abs(ratio - 1.0), 9) <= tolerance:
        return current
    return math.ceil(round(current * ratio, 6))


def desired_replicas(current, metrics, min_replicas=1, max_replicas=10, tolerance=0.1):
    if min_replicas < 1 or max_replicas < min_replicas:
        raise ValueError("require 1 <= min_replicas <= max_replicas")
    if current < 0:
        raise ValueError("current replicas cannot be negative")
    proposals = [metric_proposal(current, m, tolerance) for m in metrics]
    proposals = [p for p in proposals if p is not None]
    wanted = max(proposals) if proposals else current
    return max(min_replicas, min(max_replicas, wanted))


def bound_reason(current, metrics, min_replicas, max_replicas, tolerance=0.1):
    """Say which rule decided the final replica count."""
    result = desired_replicas(current, metrics, min_replicas, max_replicas, tolerance)
    unbounded = desired_replicas(current, metrics, 1, 10**9, tolerance)
    if result == current and unbounded == current:
        return "steady"
    if unbounded < min_replicas:
        return "min bound"
    if unbounded > max_replicas:
        return "max bound"
    return "metrics"


class Autoscaler:
    """Wraps desired_replicas with a scale-down stabilization window."""

    def __init__(self, min_replicas, max_replicas, tolerance=0.1, stabilization=300.0):
        self.min_replicas = min_replicas
        self.max_replicas = max_replicas
        self.tolerance = tolerance
        self.stabilization = stabilization
        self.recommendations = []

    def decide(self, current, metrics, now):
        raw = desired_replicas(current, metrics, self.min_replicas, self.max_replicas, self.tolerance)
        self.recommendations.append((now, raw))
        self.recommendations = [(t, r) for t, r in self.recommendations if now - t <= self.stabilization]
        if raw < current:
            return min(current, max(r for _, r in self.recommendations))
        return min(raw, self.scale_up_ceiling(current))

    @staticmethod
    def scale_up_ceiling(current):
        """One decision may at most double the fleet, or add four pods when it is small."""
        return max(current * 2, current + 4)

    def history_summary(self):
        if not self.recommendations:
            return {"samples": 0, "highest": None, "lowest": None}
        values = [r for _, r in self.recommendations]
        return {"samples": len(values), "highest": max(values), "lowest": min(values)}

    def explain(self, current, metrics):
        lines = []
        for metric in metrics:
            proposal = metric_proposal(current, metric, self.tolerance)
            shown = "no data" if proposal is None else f"{proposal} replicas"
            lines.append(f"{metric.name}: {shown}")
        return lines
