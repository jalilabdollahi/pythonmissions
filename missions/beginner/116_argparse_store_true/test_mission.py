import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import parse_args, describe, main


def test_dry_run_flag_needs_no_value():
    args = parse_args(["web", "--dry-run"])
    assert args.dry_run is True, "a switch should use action='store_true'"


def test_flag_in_the_middle_does_not_swallow_the_next_option():
    args = parse_args(["--dry-run", "--force", "web"])
    assert args.dry_run is True and args.force is True and args.target == "web"


def test_switches_default_to_false():
    args = parse_args(["web"])
    assert args.dry_run is False
    assert args.force is False


def test_describe_dry_run():
    assert describe(parse_args(["web", "--dry-run"])) == "DRY RUN: would deploy web"


def test_describe_forced_real_deploy():
    assert describe(parse_args(["web", "--force"])) == "deploying web (forced)"
    assert describe(parse_args(["web"])) == "deploying web"


def test_main_prints_description(capsys):
    assert main(["db", "--dry-run"]) == 0
    assert "DRY RUN: would deploy db" in capsys.readouterr().out
