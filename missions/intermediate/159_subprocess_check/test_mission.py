import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_successful_probe_is_ok():
    result = broken.run_probe("print('alive')")
    assert result["ok"] is True
    assert result["code"] == 0


def test_stdout_is_text_without_trailing_newline():
    result = broken.run_probe("print('alive')")
    assert result["stdout"] == "alive", "stdout must be str and stripped"


def test_nonzero_exit_without_stderr_is_a_failure():
    result = broken.run_probe("import sys; sys.exit(3)")
    assert result["ok"] is False, "the exit code is the verdict"
    assert result["code"] == 3


def test_warning_on_stderr_does_not_fail_a_zero_exit():
    result = broken.run_probe("import sys; sys.stderr.write('deprecated\\n')")
    assert result["ok"] is True
    assert result["stderr"] == "deprecated"


def test_crash_reports_the_error_text():
    result = broken.run_probe("raise RuntimeError('db unreachable')")
    assert result["ok"] is False
    assert "db unreachable" in result["stderr"]
    assert result["code"] == 1


def test_gate_returns_failed_probe_names_in_order():
    probes = {
        "db": "import sys; sys.exit(2)",
        "cache": "print('ok')",
        "queue": "raise SystemExit(1)",
        "warn": "import sys; sys.stderr.write('w')",
    }
    assert broken.gate(probes) == ["db", "queue"]
