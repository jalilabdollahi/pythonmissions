# Mission 032 - Solution

def filter_critical(alerts):
    return [a for a in alerts if a["severity"] == "CRITICAL"]

if __name__ == "__main__":
    alerts = [
        {"msg": "disk full", "severity": "CRITICAL"},
        {"msg": "high cpu", "severity": "WARN"},
        {"msg": "OOM", "severity": "CRITICAL"},
    ]
    print(filter_critical(alerts))
