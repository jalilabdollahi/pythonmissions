import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import evaluate, main


def test_all_checks_pass_returns_zero(capsys):
    assert main(["--disk", "50", "--memory", "40"]) == 0
    out = capsys.readouterr().out
    assert "PASS disk 50%" in out and "PASS memory 40%" in out


def test_failing_disk_returns_one(capsys):
    assert main(["--disk", "95", "--memory", "10"]) == 1, "pipelines read the exit status, not the printed text"
    assert "FAIL disk 95%" in capsys.readouterr().out


def test_failing_memory_returns_one(capsys):
    assert main(["--disk", "10", "--memory", "99"]) == 1


def test_all_checks_are_printed_even_after_a_failure(capsys):
    main(["--disk", "99", "--memory", "99"])
    out = capsys.readouterr().out
    assert "FAIL disk 99%" in out and "FAIL memory 99%" in out


def test_usage_at_the_limit_fails():
    results = dict((name, ok) for name, _, ok in evaluate(90, 85))
    assert results == {"disk": False, "memory": False}


def test_usage_just_below_the_limit_passes():
    results = dict((name, ok) for name, _, ok in evaluate(89, 84))
    assert results == {"disk": True, "memory": True}
