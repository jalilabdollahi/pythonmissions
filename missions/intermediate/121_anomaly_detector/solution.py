# Mission 121 - Anomaly Detector
# Fixed solution
import statistics

def z_score(value, data):
    mean = statistics.mean(data)
    std = statistics.stdev(data) if len(data) > 1 else 0
    if std == 0:
        return 0.0
    return (value - mean) / std

def detect_anomalies(data, threshold=3.0):
    anomalies = []
    for i, value in enumerate(data):
        z = z_score(value, data)
        if abs(z) > threshold:
            anomalies.append({"index": i, "value": value, "z_score": z})
    return anomalies
