import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_level_correct():
    from broken import FileLogger
    fl = FileLogger("/var/log/app.log", "INFO", "%(msg)s")
    assert fl.level == "INFO"

def test_fmt_correct():
    from broken import FileLogger
    fl = FileLogger("/var/log/app.log", "INFO", "%(msg)s")
    assert fl.fmt == "%(msg)s"

def test_path_set():
    from broken import FileLogger
    fl = FileLogger("/var/log/app.log", "INFO", "%(msg)s")
    assert fl.path == "/var/log/app.log"
