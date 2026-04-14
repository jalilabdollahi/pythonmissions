import pytest, sys
sys.path.insert(0, ".")
from broken import z_score, detect_anomalies

def test_z_score_normal():
    data = [1, 2, 3, 4, 5]
    assert abs(z_score(3, data)) < 1.0  # mean is 3

def test_z_score_extreme():
    data = [1, 2, 3, 4, 100]
    assert z_score(100, data) > 2.0

def test_z_score_uniform():
    data = [5, 5, 5, 5, 5]
    assert z_score(5, data) == 0.0

def test_detect_anomalies():
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 100]
    anomalies = detect_anomalies(data, threshold=2.0)
    values = [a["value"] for a in anomalies]
    assert 100 in values
