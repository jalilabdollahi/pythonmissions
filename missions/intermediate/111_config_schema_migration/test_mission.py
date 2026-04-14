import pytest, sys
sys.path.insert(0, ".")
from broken import MigrationRunner

def test_applies_migrations_in_order():
    runner = MigrationRunner()
    log = []
    runner.register("1.0", lambda c: (log.append("1.0"), c)[1])
    runner.register("1.1", lambda c: (log.append("1.1"), c)[1])
    runner.register("2.0", lambda c: (log.append("2.0"), c)[1])
    config = {"version": "0.9"}
    runner.run(config)
    assert log == ["1.0", "1.1", "2.0"]

def test_skips_old_versions():
    runner = MigrationRunner()
    log = []
    runner.register("1.0", lambda c: (log.append("1.0"), c)[1])
    runner.register("2.0", lambda c: (log.append("2.0"), c)[1])
    config = {"version": "1.5"}
    runner.run(config)
    assert log == ["2.0"]

def test_version_ordering():
    runner = MigrationRunner()
    assert runner._version_key("1.10") > runner._version_key("1.9")
