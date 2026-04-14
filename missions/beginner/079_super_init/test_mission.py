import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_name_set():
    from broken import MonitoredService
    svc = MonitoredService("web", "localhost", 8080, 30)
    assert svc.name == "web"

def test_interval_set():
    from broken import MonitoredService
    svc = MonitoredService("web", "localhost", 8080, 30)
    assert svc.check_interval == 30

def test_describe():
    from broken import MonitoredService
    svc = MonitoredService("web", "localhost", 8080, 30)
    desc = svc.describe()
    assert "web" in desc and "8080" in desc
