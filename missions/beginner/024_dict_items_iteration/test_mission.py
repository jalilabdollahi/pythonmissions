import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import listening_lines, services_on_port, highest_port

PORTS = {"ssh": 22, "http": 80, "metrics": 9100, "alt-http": 80}


def test_lines_are_service_colon_port():
    assert listening_lines({"ssh": 22}) == ["ssh:22"]


def test_lines_are_sorted_by_service():
    assert listening_lines(PORTS) == ["alt-http:80", "http:80", "metrics:9100", "ssh:22"]


def test_empty_dict_has_no_lines():
    assert listening_lines({}) == []


def test_services_sharing_a_port():
    assert services_on_port(PORTS, 80) == ["alt-http", "http"]
    assert services_on_port(PORTS, 1) == []


def test_highest_port_pair():
    assert highest_port(PORTS) == ("metrics", 9100)
    assert highest_port({}) is None
