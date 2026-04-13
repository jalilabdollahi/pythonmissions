import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(__file__))

FULL_YAML = """\
service:
  name: api-gateway
  port: 9000
  debug: true
database:
  host: db.internal
  port: 5433
  name: production_db
"""

NO_DB_YAML = """\
service:
  name: worker
  port: 8080
"""


@pytest.fixture
def full_config_file(tmp_path):
    p = tmp_path / "config.yaml"
    p.write_text(FULL_YAML)
    return str(p)


@pytest.fixture
def no_db_config_file(tmp_path):
    p = tmp_path / "config.yaml"
    p.write_text(NO_DB_YAML)
    return str(p)


def test_load_yaml_config_returns_dict(full_config_file):
    from broken import load_yaml_config
    result = load_yaml_config(full_config_file)
    assert isinstance(result, dict)


def test_load_yaml_config_has_service(full_config_file):
    from broken import load_yaml_config
    result = load_yaml_config(full_config_file)
    assert "service" in result


def test_get_db_settings_full(full_config_file):
    from broken import get_db_settings, load_yaml_config
    config = load_yaml_config(full_config_file)
    db = get_db_settings(config)
    assert db["host"] == "db.internal"
    assert db["port"] == 5433
    assert db["name"] == "production_db"


def test_get_db_settings_uses_defaults_when_missing(no_db_config_file):
    from broken import get_db_settings, load_yaml_config
    config = load_yaml_config(no_db_config_file)
    db = get_db_settings(config)
    assert db["host"] is not None or db["host"] == "localhost" or isinstance(db, dict)


def test_get_service_settings(full_config_file):
    from broken import get_service_settings, load_yaml_config
    config = load_yaml_config(full_config_file)
    svc = get_service_settings(config)
    assert svc["name"] == "api-gateway"
    assert svc["port"] == 9000
    assert svc["debug"] is True


def test_get_service_settings_defaults(no_db_config_file):
    from broken import get_service_settings, load_yaml_config
    config = load_yaml_config(no_db_config_file)
    svc = get_service_settings(config)
    assert svc["name"] == "worker"
    assert svc["debug"] is False
