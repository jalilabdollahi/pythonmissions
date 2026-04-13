import os
import sys

sys.path.insert(0, os.path.dirname(__file__))


def test_subject_contains_service():
    from broken import format_deploy_message
    msg = format_deploy_message("api", "1.0.0", "staging", "ali")
    assert "api" in msg["subject"]


def test_subject_contains_version():
    from broken import format_deploy_message
    msg = format_deploy_message("api", "1.0.0", "staging", "ali")
    assert "1.0.0" in msg["subject"]


def test_subject_contains_environment():
    from broken import format_deploy_message
    msg = format_deploy_message("api", "1.0.0", "staging", "ali")
    assert "staging" in msg["subject"]


def test_body_contains_deployer():
    from broken import format_deploy_message
    msg = format_deploy_message("api", "1.0.0", "staging", "jalil")
    assert "jalil" in msg["body"]


def test_returns_dict_with_keys():
    from broken import format_deploy_message
    msg = format_deploy_message("svc", "2.0", "prod", "user")
    assert "subject" in msg
    assert "body" in msg
    assert "timestamp" in msg
    assert "full" in msg


def test_full_message_combines_all():
    from broken import format_deploy_message
    msg = format_deploy_message("svc", "2.0", "prod", "tester")
    assert "svc" in msg["full"]
    assert "tester" in msg["full"]
