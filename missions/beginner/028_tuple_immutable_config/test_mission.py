import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import BASE_ARGS, launch_command, quiet_variant, with_extra_args


def test_extra_args_are_appended():
    result = with_extra_args(BASE_ARGS, ("--prefetch", "10"))
    assert result == BASE_ARGS + ("--prefetch", "10")


def test_extra_args_returns_a_tuple():
    assert isinstance(with_extra_args(BASE_ARGS, ["--x"]), tuple)


def test_quiet_variant_sets_error_level():
    result = quiet_variant(BASE_ARGS)
    assert result[result.index("--log-level") + 1] == "error"
    assert "--workers" in result, "other flags must survive"


def test_base_args_never_modified():
    with_extra_args(BASE_ARGS, ("--debug",))
    quiet_variant(BASE_ARGS)
    assert BASE_ARGS == ("--workers", "4", "--log-level", "info", "--no-color"), "defaults must stay untouched"


def test_launch_command_joins_flags():
    cmd = launch_command("quill-worker", with_extra_args(("--a",), ("--b",)))
    assert cmd == "quill-worker --a --b"
