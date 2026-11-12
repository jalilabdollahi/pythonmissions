import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken

DEFAULTS = {"workers": 2, "region": "eu-1", "debug": False}
FILE = {"workers": 4, "region": "us-2"}
ENV = {"workers": "6"}


def test_cli_beats_env_file_and_defaults():
    cfg = broken.resolve(DEFAULTS, FILE, ENV, {"workers": 8})
    assert broken.worker_count(cfg) == 8


def test_env_beats_file_and_defaults():
    cfg = broken.resolve(DEFAULTS, FILE, ENV, {})
    assert broken.worker_count(cfg) == 6


def test_file_beats_defaults():
    cfg = broken.resolve(DEFAULTS, FILE, {}, {})
    assert cfg["region"] == "us-2"
    assert broken.worker_count(cfg) == 4


def test_defaults_are_the_last_resort():
    cfg = broken.resolve(DEFAULTS, {}, {}, {})
    assert cfg["debug"] is False
    assert broken.worker_count(cfg) == 2


def test_unset_cli_options_do_not_hide_lower_layers():
    cfg = broken.resolve(DEFAULTS, FILE, ENV, {"workers": None, "region": None})
    assert broken.worker_count(cfg) == 6
    assert cfg["region"] == "us-2", "None means 'flag not given'"


def test_falsy_but_given_cli_values_still_win():
    cfg = broken.resolve(DEFAULTS, FILE, ENV, {"workers": 0, "debug": True})
    assert cfg["workers"] == 0
    assert cfg["debug"] is True


def test_effective_returns_a_flat_dict_of_winners():
    cfg = broken.resolve(DEFAULTS, FILE, ENV, {"debug": True})
    assert broken.effective(cfg) == {"workers": "6", "region": "us-2", "debug": True}


def test_inputs_are_left_untouched():
    defaults = dict(DEFAULTS)
    cfg = broken.resolve(defaults, FILE, ENV, {"workers": 1})
    cfg["extra"] = 1
    assert defaults == DEFAULTS


def test_debug_flag_from_environment_strings():
    off = broken.resolve(DEFAULTS, FILE, {"debug": "false"}, {})
    on = broken.resolve(DEFAULTS, FILE, {"debug": "yes"}, {})
    assert broken.debug_enabled(off) is False, "the string 'false' is truthy in Python"
    assert broken.debug_enabled(on) is True
    assert broken.debug_enabled(broken.resolve({}, {}, {}, {"debug": True})) is True


def test_missing_required_keys():
    cfg = broken.resolve(DEFAULTS, {}, {}, {})
    assert broken.missing_required(cfg, ["workers", "token", "api_url"]) == ["api_url", "token"]


def test_describe_sources_names_the_winning_layer():
    cfg = broken.resolve(DEFAULTS, FILE, ENV, {"debug": True})
    assert broken.describe_sources(cfg) == {"workers": "env", "region": "file", "debug": "cli"}
