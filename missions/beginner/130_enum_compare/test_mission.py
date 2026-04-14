import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_running_is_true():
    from broken import is_running, ServiceState
    assert is_running(ServiceState.RUNNING) is True

def test_stopped_is_false():
    from broken import is_running, ServiceState
    assert is_running(ServiceState.STOPPED) is False

def test_degraded_is_false():
    from broken import is_running, ServiceState
    assert is_running(ServiceState.DEGRADED) is False
