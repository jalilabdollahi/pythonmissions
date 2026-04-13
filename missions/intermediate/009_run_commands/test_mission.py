import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(__file__))


def test_run_command_returns_tuple():
    from broken import run_command
    result = run_command("echo hello")
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_run_command_captures_output():
    from broken import run_command
    output, code = run_command("echo hello world")
    assert output is not None
    assert "hello world" in output


def test_run_command_returns_string():
    from broken import run_command
    output, code = run_command("echo test")
    assert isinstance(output, str)


def test_run_command_exit_code_zero():
    from broken import run_command
    _, code = run_command("echo ok")
    assert code == 0


def test_run_command_exit_code_nonzero():
    from broken import run_command
    _, code = run_command("false")
    assert code != 0


def test_run_and_check_raises_on_failure():
    from broken import run_and_check
    with pytest.raises(RuntimeError):
        run_and_check("false")


def test_run_command_list_form():
    from broken import run_command
    output, code = run_command(["echo", "list", "form"])
    assert "list" in output
    assert code == 0
