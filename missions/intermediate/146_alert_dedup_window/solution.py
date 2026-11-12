# Mission 146 - Noisy Pager (solution)
# Suppress repeated alerts with the same fingerprint inside a time window.


def fingerprint(alert):
    labels = alert["labels"]
    pairs = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
    return f"{alert['name']}|{pairs}"


class AlertDeduper:
    def __init__(self, window_seconds):
        self.window = window_seconds
        self.last_sent = {}
        self.suppressed = {}

    def should_send(self, alert):
        fp = fingerprint(alert)
        now = alert["ts"]
        last = self.last_sent.get(fp)
        if last is not None and now - last < self.window:
            self.suppressed[fp] = self.suppressed.get(fp, 0) + 1
            return False
        self.last_sent[fp] = now
        return True

    def filter(self, alerts):
        return [a for a in alerts if self.should_send(a)]

    def total_suppressed(self):
        return sum(self.suppressed.values())
