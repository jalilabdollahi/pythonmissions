import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import Server, databases, addresses


def test_constructor_stores_host():
    assert Server("web-1", 80).host == "web-1", "assign to self.host, not a local variable"


def test_constructor_stores_port():
    assert Server("web-1", 80).port == 80


def test_role_defaults_to_web():
    assert Server("web-1", 80).role == "web"


def test_role_can_be_overridden():
    assert Server("pg-1", 5432, role="db").role == "db"


def test_address():
    assert Server("web-1", 80).address() == "web-1:80"


def test_is_database_depends_on_role():
    assert Server("pg", 5432, "db").is_database()
    assert not Server("w", 80).is_database()


def test_describe_and_helpers():
    fleet = [Server("web-1", 80), Server("pg-1", 5432, "db")]
    assert fleet[1].describe() == "db server at pg-1:5432"
    assert [s.host for s in databases(fleet)] == ["pg-1"]
    assert addresses(fleet) == ["pg-1:5432", "web-1:80"]
