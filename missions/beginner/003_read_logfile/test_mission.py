import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(__file__))

SAMPLE_LOG = """2024-01-10 10:00:01 INFO  Server started on port 8080
2024-01-10 10:00:05 INFO  Connected to database
2024-01-10 10:01:12 ERROR Could not reach upstream service
2024-01-10 10:01:13 WARN  Retrying in 5 seconds
2024-01-10 10:01:18 ERROR Upstream timeout after 5s
2024-01-10 10:02:00 INFO  Health check passed
2024-01-10 10:02:30 ERROR Disk usage above 90%
2024-01-10 10:03:00 INFO  Backup started
2024-01-10 10:03:45 INFO  Backup completed
2024-01-10 10:04:00 INFO  All systems nominal
2024-01-10 10:05:00 INFO  Scheduled job ran
2024-01-10 10:06:00 INFO  Cache cleared
"""


@pytest.fixture
def logfile(tmp_path):
    p = tmp_path / "app.log"
    p.write_text(SAMPLE_LOG)
    return str(p)


def test_count_errors_correct(logfile):
    from broken import count_errors
    assert count_errors(logfile) == 3


def test_count_errors_zero_on_clean_log(tmp_path):
    from broken import count_errors
    p = tmp_path / "clean.log"
    p.write_text("INFO hello\nINFO world\n")
    assert count_errors(str(p)) == 0


def test_last_lines_returns_correct_count(logfile):
    from broken import last_lines
    result = last_lines(logfile, 3)
    assert len(result) == 3


def test_last_lines_returns_actual_last_lines(logfile):
    from broken import last_lines
    result = last_lines(logfile, 2)
    assert "10:06:00" in result[-1]
    assert "10:05:00" in result[-2]


def test_last_lines_default_10(logfile):
    from broken import last_lines
    result = last_lines(logfile)
    assert len(result) == 10
