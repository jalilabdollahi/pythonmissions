import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import url_parts, probe_target, is_secure


def test_explicit_port_is_used():
    assert url_parts("http://metrics.local:9090/graph") == {"scheme": "http", "host": "metrics.local", "port": 9090}


def test_https_default_port_is_443():
    assert url_parts("https://svc.local/health")["port"] == 443, "no explicit port: use the scheme default"


def test_query_without_path_does_not_leak_into_host():
    assert url_parts("https://api.example.com?x=1")["host"] == "api.example.com"


def test_credentials_are_not_part_of_host():
    parts = url_parts("http://deploy@build.local:8080/job")
    assert parts["host"] == "build.local" and parts["port"] == 8080


def test_ipv6_host_without_brackets():
    parts = url_parts("http://[::1]:8000/")
    assert parts["host"] == "::1" and parts["port"] == 8000


def test_ssh_default_and_probe_target():
    assert probe_target("ssh://bastion") == "bastion:22"
    assert probe_target("http://a.b/c") == "a.b:80"


def test_is_secure():
    assert is_secure("https://x.y/") is True
    assert is_secure("http://x.y/") is False
