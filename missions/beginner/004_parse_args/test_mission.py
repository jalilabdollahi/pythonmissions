import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))


def make_args(env="staging", version="latest", dry_run=False):
    return argparse.Namespace(env=env, version=version, dry_run=dry_run)


def test_run_deploy_normal():
    from broken import run_deploy
    args = make_args(env="staging", version="1.2.3")
    result = run_deploy(args)
    assert "staging" in result
    assert "1.2.3" in result


def test_run_deploy_production():
    from broken import run_deploy
    args = make_args(env="production", version="2.0.0")
    result = run_deploy(args)
    assert "production" in result


def test_run_deploy_dry_run():
    from broken import run_deploy
    args = make_args(env="staging", dry_run=True)
    result = run_deploy(args)
    assert "DRY RUN" in result.upper() or "dry" in result.lower()


def test_run_deploy_returns_string():
    from broken import run_deploy
    args = make_args()
    assert isinstance(run_deploy(args), str)


def test_create_parser_has_env_arg():
    from broken import create_parser
    parser = create_parser()
    args = parser.parse_args(["--env", "staging"])
    assert hasattr(args, "env")
    assert args.env == "staging"
