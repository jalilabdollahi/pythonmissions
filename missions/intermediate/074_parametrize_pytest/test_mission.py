import pytest, sys
sys.path.insert(0, ".")
from broken import validate_port, classify_port

@pytest.mark.parametrize("port,expected", [
    (80, True),
    (443, True),
    (65535, True),
    (0, False),
    (65536, False),
    (-1, False),
])
def test_validate_port(port, expected):
    assert validate_port(port) == expected

@pytest.mark.parametrize("port,category", [
    (22, "system"),
    (8080, "registered"),
    (55000, "dynamic"),
])
def test_classify_port(port, category):
    assert classify_port(port) == category
