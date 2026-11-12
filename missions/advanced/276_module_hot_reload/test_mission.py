import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import PluginHost

PREFIX = "hr_"


@pytest.fixture(autouse=True)
def clean_modules():
    yield
    for name in [n for n in sys.modules if n.startswith(PREFIX)]:
        del sys.modules[name]


@pytest.fixture
def plugdir(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(tmp_path))
    return tmp_path


def write(directory, name, body, bump=0):
    path = directory / (name + ".py")
    path.write_text(body)
    if bump:
        st = os.stat(path)
        os.utime(path, ns=(st.st_atime_ns, st.st_mtime_ns + bump * 10**9))
    return path


def echo(version):
    return f"def handle(payload):\n    return '{version}:' + payload\n"


def test_discovers_and_dispatches_plugins(plugdir):
    write(plugdir, "hr_alpha", echo("a1"))
    write(plugdir, "_private", "x = 1\n")
    host = PluginHost(plugdir)
    assert host.load_new() == ["hr_alpha"]
    assert host.dispatch("hr_alpha", "ping") == "a1:ping"
    assert host.loaded() == ["hr_alpha"]


def test_edited_plugin_is_reloaded_and_new_code_is_used(plugdir):
    path = write(plugdir, "hr_beta", echo("v1"))
    host = PluginHost(plugdir)
    host.load_new()
    assert host.refresh() == [], "nothing changed yet"
    write(plugdir, "hr_beta", echo("v2"), bump=10)
    assert host.refresh() == ["hr_beta"]
    assert host.dispatch("hr_beta", "x") == "v2:x", "the dispatch table must follow the reloaded module"


def test_unchanged_mtime_means_no_reload(plugdir):
    write(plugdir, "hr_gamma", echo("g"))
    host = PluginHost(plugdir)
    host.load_new()
    host.refresh()
    host.refresh()
    assert host.reload_attempts == 0


def test_new_plugin_file_is_found_even_if_directory_listing_is_cached(plugdir):
    tick = 1_700_000_000 * 10**9
    write(plugdir, "hr_one", echo("one"))
    os.utime(plugdir, ns=(tick, tick))
    host = PluginHost(plugdir)
    host.load_new()
    write(plugdir, "hr_two", echo("two"))
    os.utime(plugdir, ns=(tick, tick))  # a coarse filesystem clock: same directory mtime as at the first scan
    assert host.refresh() == ["hr_two"], "the import system's directory cache must be invalidated"
    assert host.dispatch("hr_two", "!") == "two:!"


def test_removed_plugin_is_forgotten_everywhere(plugdir):
    path = write(plugdir, "hr_gone", echo("gone"))
    host = PluginHost(plugdir)
    host.load_new()
    path.unlink()
    assert host.refresh() == ["hr_gone"]
    assert host.loaded() == []
    assert "hr_gone" not in sys.modules, "a stale module object would resurrect old code on re-add"
    with pytest.raises(KeyError):
        host.dispatch("hr_gone", "x")
    write(plugdir, "hr_gone", echo("reborn"))
    assert host.refresh() == ["hr_gone"]
    assert host.dispatch("hr_gone", "x") == "reborn:x"


def test_broken_edit_keeps_old_version_serving_and_is_tried_only_once(plugdir):
    write(plugdir, "hr_delta", echo("good"))
    host = PluginHost(plugdir)
    host.load_new()
    write(plugdir, "hr_delta", "def handle(payload:\n    return 1\n", bump=5)
    assert host.refresh() == []
    assert "SyntaxError" in host.errors["hr_delta"]
    assert host.dispatch("hr_delta", "q") == "good:q"
    host.refresh()
    host.refresh()
    assert host.reload_attempts == 1, "do not retry a broken file on every poll until it changes again"


def test_fixing_a_broken_plugin_clears_the_error(plugdir):
    write(plugdir, "hr_eps", echo("one"))
    host = PluginHost(plugdir)
    host.load_new()
    write(plugdir, "hr_eps", "raise RuntimeError('boom')\n", bump=5)
    host.refresh()
    assert "RuntimeError" in host.errors["hr_eps"]
    write(plugdir, "hr_eps", echo("two"), bump=10)
    assert host.refresh() == ["hr_eps"]
    assert host.errors == {}
    assert host.dispatch("hr_eps", "z") == "two:z"
