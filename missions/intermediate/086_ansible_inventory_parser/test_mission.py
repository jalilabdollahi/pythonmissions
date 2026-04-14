import pytest, sys
sys.path.insert(0, ".")
from broken import parse_inventory, get_hosts_in_group, get_host_var

INVENTORY = """
[webservers]
web-01 ansible_user=ubuntu ansible_port=22
web-02 ansible_user=ubuntu

[dbservers]
db-01 ansible_user=postgres
"""

def test_parse_groups():
    inv = parse_inventory(INVENTORY)
    assert "webservers" in inv
    assert "dbservers" in inv

def test_get_hosts():
    inv = parse_inventory(INVENTORY)
    hosts = get_hosts_in_group(inv, "webservers")
    assert "web-01" in hosts
    assert "web-02" in hosts

def test_get_var():
    inv = parse_inventory(INVENTORY)
    port = get_host_var(inv, "webservers", "web-01", "ansible_port")
    assert port == "22"
