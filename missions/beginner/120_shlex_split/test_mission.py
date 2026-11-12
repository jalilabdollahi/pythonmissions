import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import parse_command, flag_value, program_name, describe

COMMIT = 'git commit -m "fix login bug" --author=\'Ana Gomez\' --no-verify'


def test_plain_words_split_on_spaces():
    assert parse_command("ls -la /var/log") == ["ls", "-la", "/var/log"]


def test_double_quoted_argument_stays_together():
    assert parse_command('git commit -m "fix login bug"') == ["git", "commit", "-m", "fix login bug"], "use shlex.split"


def test_single_quotes_are_handled_and_removed():
    assert parse_command(COMMIT)[4] == "--author=Ana Gomez"


def test_flag_value_returns_whole_quoted_message():
    assert flag_value(COMMIT, "-m") == "fix login bug"


def test_missing_or_last_flag_gives_none():
    assert flag_value(COMMIT, "--force") is None
    assert flag_value("deploy --env", "--env") is None


def test_program_name_and_describe():
    assert program_name(COMMIT) == "git"
    assert program_name("") == ""
    assert describe(COMMIT) == "git with 5 arguments"
