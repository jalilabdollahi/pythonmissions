# Mission 264 - Ticket Sale Burn Alarm
# Multi-window, multi-burn-rate SLO alerting for a ticketing API.

SLO_TARGET = 0.999  # 99.9% of requests succeed over the 30-day period
PERIOD_HOURS = 30 * 24

# (long window seconds, short window seconds, burn-rate threshold, severity)
POLICIES = [
    (3600, 300, 14.4, "page"),
    (21600, 1800, 6.0, "page"),
    (259200, 21600, 1.0, "ticket"),
]


def window_counts(buckets, now, seconds):
    """buckets: list of (ts, total, errors). Sum those in (now - seconds, now]."""
    total = errors = 0
    for ts, t, e in buckets:
        if now - seconds < ts <= now:
            total += t
            errors += e
    return total, errors


def error_ratio(buckets, now, seconds):
    total, errors = window_counts(buckets, now, seconds)
    if total == 0:
        return 1.0
    return errors / (total - errors)


def burn_rate(ratio, slo=SLO_TARGET):
    """1.0 means the error budget is being spent exactly as fast as it accrues."""
    budget = slo
    return ratio / budget


def evaluate(buckets, now, slo=SLO_TARGET):
    """Return the list of firing alerts for the given traffic."""
    alerts = []
    for long_s, short_s, threshold, severity in POLICIES:
        long_burn = burn_rate(error_ratio(buckets, now, long_s), slo)
        short_burn = burn_rate(error_ratio(buckets, now, short_s), slo)
        if long_burn >= threshold or short_burn >= threshold:
            alerts.append(
                {
                    "severity": severity,
                    "window": long_s,
                    "burn": round(long_burn, 2),
                    "threshold": threshold,
                }
            )
    return alerts


def hours_to_exhaustion(burn):
    """Hours until a full period budget is gone at a constant burn rate."""
    if burn <= 0:
        return None
    return PERIOD_HOURS / burn


def top_severity(alerts):
    if any(a["severity"] == "page" for a in alerts):
        return "page"
    if alerts:
        return "ticket"
    return "ok"


def steady_traffic(start, end, per_minute, error_rate_at):
    """Build minute buckets; error_rate_at(ts) gives the failure fraction."""
    out = []
    for ts in range(start, end + 1, 60):
        out.append((ts, per_minute, round(per_minute * error_rate_at(ts))))
    return out


if __name__ == "__main__":
    data = steady_traffic(0, 7200, 1000, lambda ts: 0.02 if ts > 6000 else 0.0005)
    print(top_severity(evaluate(data, 7200)))
