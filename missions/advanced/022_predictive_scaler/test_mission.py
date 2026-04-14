import pytest, sys
sys.path.insert(0, ".")
from broken import PredictiveScaler

def test_scale_up_on_forecast():
    scaler = PredictiveScaler(min_replicas=1, max_replicas=20, threshold=0.5)
    for load in [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
        scaler.record(load)
    desired = scaler.desired_replicas(3)
    assert desired > 3  # trending up, should scale out

def test_scale_down_bounded():
    scaler = PredictiveScaler(min_replicas=2, max_replicas=20)
    for _ in range(10):
        scaler.record(0.1)
    desired = scaler.desired_replicas(2)
    assert desired >= 2  # never below min_replicas

def test_forecast_trend():
    scaler = PredictiveScaler()
    for i in range(10):
        scaler.record(i * 0.05)
    pred = scaler.forecast(steps_ahead=1)
    assert pred > scaler.history[-1]  # trending upward
