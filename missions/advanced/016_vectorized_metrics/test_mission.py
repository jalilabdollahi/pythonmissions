import pytest, sys
sys.path.insert(0, ".")
from broken import MetricsProcessor

def test_per_service_average():
    p = MetricsProcessor()
    data = [[10, 20, 30], [40, 50, 60]]  # 2 services, 3 time points
    result = p.per_service_average(data)
    assert result[0] == 20.0  # avg of first service: (10+20+30)/3
    assert result[1] == 50.0  # avg of second service

def test_normalize():
    p = MetricsProcessor()
    result = p.normalize([0, 5, 10])
    assert result[0] == 0.0
    assert result[-1] == 1.0
    assert result[1] == 0.5
