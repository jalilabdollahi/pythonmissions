import os
import sys

sys.path.insert(0, os.path.dirname(__file__))


def test_get_server_info_returns_dict():
    from broken import get_server_info
    info = get_server_info()
    assert isinstance(info, dict)


def test_get_server_info_has_server_key():
    from broken import get_server_info
    info = get_server_info()
    assert info["server"] == "prod-web-01"


def test_get_server_info_has_port():
    from broken import get_server_info
    info = get_server_info()
    assert info["port"] == 8080


def test_get_server_info_has_env():
    from broken import get_server_info
    info = get_server_info()
    assert info["env"] == "production"


def test_main_runs_without_error(capsys):
    from broken import main
    main()
    captured = capsys.readouterr()
    assert "prod-web-01" in captured.out
    assert "8080" in captured.out
    assert "production" in captured.out
