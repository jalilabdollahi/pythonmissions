# Mission 112 - Find New Alerts
def new_alerts(previous, current):
    """Return alerts in current that were not in previous."""
    return previous.symmetric_difference(current)

if __name__ == "__main__":
    prev = {"disk-full", "high-cpu"}
    curr = {"disk-full", "oom", "network-down"}
    print(new_alerts(prev, curr))
