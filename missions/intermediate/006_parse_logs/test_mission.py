import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

SAMPLE_LOGS = """\
10.0.0.1 - - [10/Jan/2024:10:00:01 +0000] "GET /api/v1 HTTP/1.1" 500 1234
10.0.0.2 - - [10/Jan/2024:10:00:02 +0000] "POST /login HTTP/1.1" 200 567
10.0.0.1 - - [10/Jan/2024:10:00:03 +0000] "GET /api/v1 HTTP/1.1" 502 890
10.0.0.3 - - [10/Jan/2024:10:00:04 +0000] "GET /health HTTP/1.1" 503 12
10.0.0.2 - - [10/Jan/2024:10:00:05 +0000] "GET /static HTTP/1.1" 404 88
10.0.0.1 - - [10/Jan/2024:10:00:06 +0000] "DELETE /api/v1 HTTP/1.1" 500 55
10.0.0.4 - - [10/Jan/2024:10:00:07 +0000] "GET /api/v1 HTTP/1.1" 200 999
"""


def test_finds_5xx_ips():
    from broken import find_5xx_ips
    ips = find_5xx_ips(SAMPLE_LOGS)
    assert "10.0.0.1" in ips
    assert "10.0.0.3" in ips


def test_excludes_non_5xx():
    from broken import find_5xx_ips
    ips = find_5xx_ips(SAMPLE_LOGS)
    assert "10.0.0.4" not in ips


def test_correct_5xx_count():
    from broken import find_5xx_ips
    ips = find_5xx_ips(SAMPLE_LOGS)
    assert ips.count("10.0.0.1") == 3


def test_top_offenders_returns_list():
    from broken import top_offenders
    result = top_offenders(SAMPLE_LOGS)
    assert isinstance(result, list)


def test_top_offenders_correct_leader():
    from broken import top_offenders
    result = top_offenders(SAMPLE_LOGS)
    assert result[0][0] == "10.0.0.1"
    assert result[0][1] == 3


def test_empty_log():
    from broken import find_5xx_ips
    assert find_5xx_ips("") == []
