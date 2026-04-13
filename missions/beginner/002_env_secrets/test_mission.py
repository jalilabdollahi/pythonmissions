import os
import sys

sys.path.insert(0, os.path.dirname(__file__))


def test_get_db_config_returns_dict():
    from broken import get_db_config
    cfg = get_db_config()
    assert isinstance(cfg, dict)


def test_default_host():
    from broken import get_db_config
    os.environ.pop("DB_HOST", None)
    cfg = get_db_config()
    assert cfg["host"] == "localhost"


def test_port_is_integer():
    from broken import get_db_config
    os.environ.pop("DB_PORT", None)
    cfg = get_db_config()
    assert isinstance(cfg["port"], int)
    assert cfg["port"] == 5432


def test_custom_host_from_env():
    from broken import get_db_config
    os.environ["DB_HOST"] = "db.prod.internal"
    cfg = get_db_config()
    assert cfg["host"] == "db.prod.internal"
    del os.environ["DB_HOST"]


def test_custom_port_from_env():
    from broken import get_db_config
    os.environ["DB_PORT"] = "5433"
    cfg = get_db_config()
    assert cfg["port"] == 5433
    assert isinstance(cfg["port"], int)
    del os.environ["DB_PORT"]


def test_connection_string_format():
    from broken import connection_string
    os.environ.pop("DB_HOST", None)
    os.environ.pop("DB_PORT", None)
    os.environ.pop("DB_NAME", None)
    s = connection_string()
    assert s == "postgresql://localhost:5432/appdb"
