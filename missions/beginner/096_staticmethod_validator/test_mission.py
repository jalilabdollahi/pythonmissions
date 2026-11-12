import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import RequestValidator, approve


def test_port_valid_on_instance():
    assert RequestValidator().is_valid_port(8080), "a staticmethod gets no automatic self"


def test_port_range_limits():
    v = RequestValidator()
    assert v.is_valid_port(1) and v.is_valid_port(65535)
    assert not v.is_valid_port(0)
    assert not v.is_valid_port(65536)


def test_port_must_be_integer():
    assert not RequestValidator().is_valid_port("80")


def test_hostname_valid_on_instance():
    assert RequestValidator().is_valid_hostname("db-1")


def test_hostname_rules():
    v = RequestValidator()
    assert not v.is_valid_hostname("")
    assert not v.is_valid_hostname("-db")
    assert not v.is_valid_hostname("db-")
    assert not v.is_valid_hostname("DB1")


def test_helpers_callable_on_the_class():
    assert RequestValidator.is_valid_port(22)
    assert RequestValidator.is_valid_hostname("web")


def test_validate_reports_problems():
    v = RequestValidator()
    assert v.validate({"host": "web", "port": 80}) == []
    assert v.validate({"host": "-x", "port": 0}) == ["bad host", "bad port"]


def test_approve_filters_requests():
    good = {"host": "api", "port": 443}
    bad = {"host": "api", "port": 70000}
    assert approve([good, bad]) == [good]
