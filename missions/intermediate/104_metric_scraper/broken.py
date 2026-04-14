# Mission 104 - Prometheus Metric Scraper
# Fix the 2 bugs in this script.

def parse_prometheus_text(text):
    """Parse Prometheus exposition format into {metric_name: value} dict."""
    metrics = {}
    for line in text.strip().splitlines():
        if line.startswith("#") or not line.strip():
            metrics["#"] = 0  # BUG 1: should skip (continue), not add a fake entry
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        name = parts[0]
        value = float(parts[1])  # BUG 2: value is last field (parts[-1]), not parts[1] — labels may be present
        metrics[name] = value
    return metrics

def get_metric(text, name, default=0.0):
    m = parse_prometheus_text(text)
    return m.get(name, default)
