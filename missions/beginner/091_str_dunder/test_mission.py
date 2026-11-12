import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import Deployment, changelog, failures


def test_str_returns_readable_line():
    assert str(Deployment("api", "2.3.1", "prod")) == "api v2.3.1 -> prod [OK]", "__str__ must return a string"


def test_str_marks_failures():
    assert str(Deployment("web", "9.0.0", "stage", ok=False)) == "web v9.0.0 -> stage [FAILED]"


def test_f_string_uses_str():
    d = Deployment("api", "1", "dev")
    assert f"{d}" == "api v1 -> dev [OK]"


def test_repr_is_unambiguous():
    assert repr(Deployment("api", "2.3.1", "prod")) == "Deployment('api', '2.3.1', 'prod')"


def test_changelog_joins_lines():
    log = [Deployment("a", "1", "p"), Deployment("b", "2", "p", False)]
    assert changelog(log) == "a v1 -> p [OK]\nb v2 -> p [FAILED]"


def test_failures_filter():
    log = [Deployment("a", "1", "p"), Deployment("b", "2", "p", False)]
    assert [d.service for d in failures(log)] == ["b"]
