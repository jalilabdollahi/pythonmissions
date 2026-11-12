import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def write(tmp_path, text):
    p = tmp_path / "worker.ini"
    p.write_text(text)
    return str(p)


def test_threads_is_an_int(tmp_path):
    s = broken.load_settings(write(tmp_path, "[worker]\nthreads = 8\n"))
    assert s["threads"] == 8 and isinstance(s["threads"], int)


def test_debug_false_is_really_false(tmp_path):
    s = broken.load_settings(write(tmp_path, "[worker]\ndebug = false\n"))
    assert s["debug"] is False, "the string 'false' is truthy; use getboolean"


def test_debug_accepts_yes_and_on_and_one(tmp_path):
    for word in ("yes", "on", "1", "True"):
        s = broken.load_settings(write(tmp_path, f"[worker]\ndebug = {word}\n"))
        assert s["debug"] is True, word


def test_timeout_float(tmp_path):
    s = broken.load_settings(write(tmp_path, "[worker]\ntimeout = 2.5\n"))
    assert s["timeout"] == 2.5


def test_missing_options_use_defaults(tmp_path):
    s = broken.load_settings(write(tmp_path, "[worker]\n"))
    assert s == {"threads": 4, "debug": False, "timeout": 30.0}


def test_missing_section_uses_defaults(tmp_path):
    s = broken.load_settings(write(tmp_path, "[other]\nx = 1\n"))
    assert s == {"threads": 4, "debug": False, "timeout": 30.0}


def test_missing_file_uses_defaults(tmp_path):
    s = broken.load_settings(str(tmp_path / "nope.ini"))
    assert s["threads"] == 4


def test_describe_text():
    text = broken.describe({"threads": 2, "debug": True, "timeout": 1.5})
    assert text == "2 threads, debug, timeout 1.5s"
