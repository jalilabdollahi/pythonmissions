# Mission 104 - Prometheus Metric Scraper
# Fixed solution

def parse_prometheus_text(text):
    metrics = {}
    for line in text.strip().splitlines():
        if line.startswith("#") or not line.strip():
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        name = parts[0]
        value = float(parts[-1])
        metrics[name] = value
    return metrics

def get_metric(text, name, default=0.0):
    m = parse_prometheus_text(text)
    return m.get(name, default)
