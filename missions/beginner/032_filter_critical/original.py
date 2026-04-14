# Mission 032 - Filter Critical Alerts
# Fix the bug.

def filter_critical(alerts):
    """Return only CRITICAL severity alerts."""
    return [a for a in alerts if a["severity"] is "CRITICAL"]

if __name__ == "__main__":
    alerts = [
        {"msg": "disk full", "severity": "CRITICAL"},
        {"msg": "high cpu", "severity": "WARN"},
        {"msg": "OOM", "severity": "CRITICAL"},
    ]
    print(filter_critical(alerts))
