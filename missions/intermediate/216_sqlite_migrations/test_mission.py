import os
import sqlite3
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken

MIGRATIONS = {
    "1": "CREATE TABLE svc (name TEXT)",
    "2": "ALTER TABLE svc ADD COLUMN owner TEXT",
    "10": "CREATE INDEX idx_owner ON svc (owner)",
}


@pytest.fixture
def conn(tmp_path):
    connection = sqlite3.connect(tmp_path / "app.db")
    yield connection
    connection.close()


def test_versions_are_applied_in_numeric_order(conn):
    assert broken.migrate(conn, MIGRATIONS) == ["1", "2", "10"], "'10' must come after '2', not after '1'"


def test_schema_is_really_changed(conn):
    broken.migrate(conn, MIGRATIONS)
    columns = [row[1] for row in conn.execute("PRAGMA table_info(svc)")]
    assert columns == ["name", "owner"]


def test_second_run_applies_nothing(conn):
    broken.migrate(conn, MIGRATIONS)
    assert broken.migrate(conn, MIGRATIONS) == []


def test_only_new_migrations_run_later(conn):
    broken.migrate(conn, {"1": MIGRATIONS["1"]})
    newer = dict(MIGRATIONS)
    assert broken.migrate(conn, newer) == ["2", "10"]


def test_failed_migration_is_not_recorded(conn):
    migrations = dict(MIGRATIONS)
    migrations["11"] = "ALTER TABLE ghost ADD COLUMN x TEXT"
    with pytest.raises(sqlite3.OperationalError):
        broken.migrate(conn, migrations)
    applied = broken.applied_versions(conn)
    assert "11" not in applied, "record a version only after its SQL succeeded"
    assert {"1", "2", "10"} <= applied


def test_current_version_is_the_numeric_maximum(conn):
    broken.ensure_table(conn)
    assert broken.current_version(conn) == 0
    broken.migrate(conn, MIGRATIONS)
    assert broken.current_version(conn) == 10
