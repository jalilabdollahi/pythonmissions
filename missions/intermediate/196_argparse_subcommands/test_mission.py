import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_purge_counts_paths():
    assert broken.main(["purge", "eu-west", "/a.css", "/b.js"]) == "purged 2 path(s) in zone eu-west"


def test_status_subcommand_dispatches():
    assert broken.main(["status", "us-east"]) == "zone us-east is serving"


def test_ttl_subcommand_is_wired_to_its_handler():
    assert broken.main(["ttl", "eu-west", "600"]) == "zone eu-west ttl set to 10 minute(s)"


def test_ttl_seconds_are_parsed_as_integers():
    args = broken.build_parser().parse_args(["ttl", "z", "120"])
    assert args.seconds == 120 and isinstance(args.seconds, int), "give the argument type=int"


def test_ttl_rejects_non_numeric_seconds():
    with pytest.raises(SystemExit) as info:
        broken.build_parser().parse_args(["ttl", "z", "soon"])
    assert info.value.code == 2


def test_missing_subcommand_is_a_usage_error():
    with pytest.raises(SystemExit) as info:
        broken.build_parser().parse_args([])
    assert info.value.code == 2, "a missing subcommand should be reported by argparse itself"
