import pytest
import sys
sys.path.insert(0, ".")
from broken import parse_log_line, get_error_rate

SAMPLE = '127.0.0.1 - - [10/Oct/2024:13:55:36 +0000] "GET /api/health HTTP/1.1" 200 1024'
ERROR_LINE = '10.0.0.1 - - [10/Oct/2024:13:55:37 +0000] "POST /login HTTP/1.1" 401 256'

def test_parse_log_line():
    result = parse_log_line(SAMPLE)
    assert result is not None
    assert result["ip"] == "127.0.0.1"
    assert result["status"] == 200

def test_error_rate():
    lines = [SAMPLE, ERROR_LINE]
    rate = get_error_rate(lines)
    assert rate == 0.5
