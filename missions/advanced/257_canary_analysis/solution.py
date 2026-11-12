# Mission 257 - Canary Verdict (solution)
# Decides whether a canary release is worse than the baseline, using a two-proportion z-test.
import math
from collections import namedtuple

Sample = namedtuple("Sample", ["requests", "errors"])
Verdict = namedtuple("Verdict", ["decision", "baseline_rate", "canary_rate", "z", "reason"])


def _validate(name, sample):
    if sample.requests < 0 or sample.errors < 0 or sample.errors > sample.requests:
        raise ValueError(f"{name}: invalid sample {sample}")


def error_rate(sample):
    return sample.errors / sample.requests if sample.requests else 0.0


def z_score(baseline, canary):
    """Two-proportion z statistic for 'canary error rate is higher than baseline'."""
    total_requests = baseline.requests + canary.requests
    pooled = (baseline.errors + canary.errors) / total_requests
    variance = pooled * (1 - pooled) * (1 / baseline.requests + 1 / canary.requests)
    if variance == 0:
        return 0.0
    return (error_rate(canary) - error_rate(baseline)) / math.sqrt(variance)


def analyze(baseline, canary, min_samples=500, z_critical=1.96, min_effect=0.005):
    _validate("baseline", baseline)
    _validate("canary", canary)
    base_rate = error_rate(baseline)
    canary_rate = error_rate(canary)
    if baseline.requests < min_samples or canary.requests < min_samples:
        return Verdict("inconclusive", base_rate, canary_rate, 0.0, "not enough traffic yet")
    z = z_score(baseline, canary)
    difference = canary_rate - base_rate
    if z >= z_critical and difference >= min_effect:
        return Verdict("rollback", base_rate, canary_rate, z, "canary errors are significantly higher")
    return Verdict("promote", base_rate, canary_rate, z, "no significant regression")


def percentile(values, pct):
    """Nearest-rank percentile of a non-empty list."""
    if not values:
        raise ValueError("no latency samples")
    ordered = sorted(values)
    rank = max(1, math.ceil(pct / 100 * len(ordered)))
    return ordered[rank - 1]


def latency_regressed(baseline_ms, canary_ms, tolerance=0.2):
    """True when the canary's p95 latency is more than `tolerance` above the baseline's."""
    return percentile(canary_ms, 95) > percentile(baseline_ms, 95) * (1 + tolerance)


def gate(baseline, canary, baseline_ms, canary_ms, **options):
    verdict = analyze(baseline, canary, **options)
    if verdict.decision == "promote" and latency_regressed(baseline_ms, canary_ms):
        return verdict._replace(decision="rollback", reason="p95 latency regressed")
    return verdict


def evaluate_rollout(stages, **options):
    """stages is a list of (baseline, canary) samples collected at growing traffic shares."""
    verdicts = []
    for baseline, canary in stages:
        verdict = analyze(baseline, canary, **options)
        verdicts.append(verdict)
        if verdict.decision == "rollback":
            return "rollback", verdicts
    if verdicts and verdicts[-1].decision == "promote":
        return "promote", verdicts
    return "wait", verdicts


def format_verdict(verdict):
    return (
        f"{verdict.decision.upper()}: baseline {verdict.baseline_rate:.2%}, "
        f"canary {verdict.canary_rate:.2%}, z={verdict.z:.2f} ({verdict.reason})"
    )
