import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_log_file():
    from broken import is_log_file
    assert is_log_file("app.log") is True

def test_yaml_file():
    from broken import is_log_file
    assert is_log_file("config.yaml") is False

def test_filter_logs():
    from broken import filter_logs
    result = filter_logs(["app.log", "config.yaml", "error.log"])
    assert result == ["app.log", "error.log"]
