import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken

SLEEPER = "import time; time.sleep(3)"


def test_quick_job_is_ok_and_returns_output():
    assert broken.run_job("print('exported 12 rows')", 5000) == {"status": "ok", "stdout": "exported 12 rows"}


def test_nonzero_exit_is_reported_as_error():
    result = broken.run_job("import sys; sys.exit(2)", 5000)
    assert result == {"status": "error", "returncode": 2}


def test_hung_job_returns_timeout_instead_of_raising():
    result = broken.run_job(SLEEPER, 300)
    assert result == {"status": "timeout"}, "TimeoutExpired must be turned into a status"


def test_timeout_argument_is_milliseconds():
    start = time.monotonic()
    result = broken.run_job(SLEEPER, 300)
    elapsed = time.monotonic() - start
    assert result["status"] == "timeout"
    assert elapsed < 2.5, "300 ms must mean 0.3 seconds, not 300 seconds"


def test_queue_continues_after_a_timeout():
    jobs = ["print(1)", SLEEPER, "raise SystemExit(5)", "print(2)"]
    assert broken.run_queue(jobs, 400) == ["ok", "timeout", "error", "ok"]
