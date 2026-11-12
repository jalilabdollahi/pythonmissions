import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import port_list, allow_rule, rules_for


def test_two_ports():
    assert port_list([80, 443]) == "80,443"


def test_single_port_has_no_comma():
    assert port_list([22]) == "22"


def test_no_ports_gives_empty_string():
    assert port_list([]) == ""


def test_allow_rule_text():
    assert allow_rule("tcp", [80, 443]) == "allow tcp 80,443"


def test_rules_sorted_by_service_name():
    services = {"web": ("tcp", [80, 443]), "dns": ("udp", [53])}
    assert rules_for(services) == ["allow udp 53", "allow tcp 80,443"]
