import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import Server, TlsServer, load_all


def test_from_string_builds_a_server():
    s = Server.from_string("db1:5432")
    assert isinstance(s, Server)
    assert s.host == "db1"


def test_port_is_converted_to_int():
    assert Server.from_string("db1:5432").port == 5432


def test_from_string_strips_whitespace():
    s = Server.from_string("  web:80\n")
    assert (s.host, s.port) == ("web", 80)


def test_subclass_factory_returns_subclass():
    s = TlsServer.from_string("web:443")
    assert type(s) is TlsServer, "use cls(...) so subclasses build themselves"


def test_urls_use_the_right_scheme():
    assert Server.from_string("a:80").url() == "http://a:80"
    assert TlsServer.from_string("a:443").url() == "https://a:443"


def test_load_all_skips_blank_lines():
    servers = load_all(Server, ["a:1", "", "b:2"])
    assert [s.host for s in servers] == ["a", "b"]


def test_load_all_uses_given_class():
    servers = load_all(TlsServer, ["a:1"])
    assert servers[0].url() == "https://a:1"
