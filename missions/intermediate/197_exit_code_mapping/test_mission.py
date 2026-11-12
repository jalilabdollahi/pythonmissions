import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_schema_error_has_its_own_code():
    assert broken.exit_code_for(broken.SchemaError("bad field")) == 3


def test_config_error_is_2_even_though_schema_error_inherits_from_it():
    assert broken.exit_code_for(broken.ConfigError("missing file")) == 2


def test_timeout_and_generic_deploy_errors():
    assert broken.exit_code_for(broken.RolloutTimeout("30s")) == 4
    assert broken.exit_code_for(broken.DeployError("boom")) == 1


def test_unknown_exceptions_use_70_not_1():
    assert broken.exit_code_for(ValueError("bug in the tool")) == 70, "1 is already taken by DeployError"


def test_run_cli_success_is_zero(capsys):
    assert broken.run_cli(lambda: None) == 0
    assert capsys.readouterr().err == ""


def test_run_cli_reports_message_on_stderr(capsys):
    def action():
        raise broken.SchemaError("replicas must be an int")

    assert broken.run_cli(action) == 3
    captured = capsys.readouterr()
    assert captured.err == "error: replicas must be an int\n"
    assert captured.out == ""


def test_ctrl_c_exits_130_without_traceback(capsys):
    def action():
        raise KeyboardInterrupt

    assert broken.run_cli(action) == 130
