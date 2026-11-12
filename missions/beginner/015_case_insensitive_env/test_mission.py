import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import is_production, count_production, by_environment

FLEET = [
    {"id": 1, "environment": "prod"},
    {"id": 2, "environment": "PROD"},
    {"id": 3, "environment": "Production"},
    {"id": 4, "environment": "prod "},
    {"id": 5, "environment": "staging"},
    {"id": 6, "environment": "Staging"},
    {"id": 7},
    {"id": 8, "environment": "preprod"},
]


def test_lowercase_prod():
    assert is_production("prod") is True


def test_uppercase_and_mixed_case_prod():
    assert is_production("PROD") is True
    assert is_production("Production") is True


def test_trailing_space_is_ignored():
    assert is_production("prod ") is True


def test_preprod_is_not_production():
    assert is_production("preprod") is False


def test_empty_and_none_are_not_production():
    assert is_production(None) is False
    assert is_production("") is False


def test_count_production_in_messy_fleet():
    assert count_production(FLEET) == 4, "every spelling of prod must be counted"


def test_by_environment_normalizes_names():
    assert by_environment(FLEET) == {"prod": 3, "production": 1, "staging": 2, "untagged": 1, "preprod": 1}
