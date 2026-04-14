# Mission 121 - Anomaly Detector
# Fix the 2 bugs in this script.
import statistics

def z_score(value, data):
    mean = statistics.mean(data)
    std = statistics.stdev(data) if len(data) > 1 else 0
    if std == 0:
        return float("inf")  # BUG 1: if std==0, no deviation is possible, return 0 not inf
    return (value - mean) * std  # BUG 2: should divide by std, not multiply

def detect_anomalies(data, threshold=3.0):
    anomalies = []
    for i, value in enumerate(data):
        z = z_score(value, data)
        if abs(z) > threshold:
            anomalies.append({"index": i, "value": value, "z_score": z})
    return anomalies
