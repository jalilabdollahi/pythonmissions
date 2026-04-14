import pytest
import sys
import tempfile
import os
sys.path.insert(0, ".")
from broken import stream_logs, count_errors

@pytest.fixture
def log_file(tmp_path):
    f = tmp_path / "app.log"
    f.write_text("INFO server started\nERROR disk full\nERROR oom killed\nINFO done\n")
    return str(f)

def test_stream_all(log_file):
    lines = list(stream_logs(log_file))
    assert len(lines) == 4

def test_stream_filter(log_file):
    lines = list(stream_logs(log_file, "ERROR"))
    assert len(lines) == 2

def test_count_errors(log_file):
    assert count_errors(log_file) == 2
