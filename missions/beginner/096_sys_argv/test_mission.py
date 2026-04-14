import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_returns_first_arg():
    from broken import get_env_arg
    assert get_env_arg(["script.py", "production"]) == "production"

def test_staging():
    from broken import get_env_arg
    assert get_env_arg(["deploy.py", "staging"]) == "staging"
