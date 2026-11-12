import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import read_port, listen_ports, needs_root


def test_port_is_an_integer():
    assert read_port({"PORT": "9090"}) == 9090
    assert isinstance(read_port({"PORT": "9090"}), int), "environment values are strings"


def test_default_port_when_unset():
    assert read_port({}) == 8000


def test_metrics_port_is_main_plus_one():
    assert listen_ports({"PORT": "9090"}) == [9090, 9091]


def test_default_listen_ports():
    assert listen_ports({}) == [8000, 8001]


def test_privileged_port_needs_root():
    assert needs_root({"PORT": "443"}) is True


def test_high_port_does_not_need_root():
    assert needs_root({"PORT": "8443"}) is False
    assert needs_root({}) is False
