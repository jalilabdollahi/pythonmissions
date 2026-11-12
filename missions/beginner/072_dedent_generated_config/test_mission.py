import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_vhost_exact_output():
    got = broken.render_vhost("shop.example", 8080)
    want = "server {\n    listen 8080;\n    server_name shop.example;\n}\n"
    assert got == want, repr(got)


def test_vhost_first_line_starts_at_column_zero():
    assert broken.render_vhost("a.example", 80).startswith("server {")


def test_vhost_lines_have_four_space_indent():
    lines = broken.render_vhost("a.example", 80).splitlines()
    assert lines[1].startswith("    listen") and not lines[1].startswith("     ")


def test_upstream_exact_output():
    got = broken.render_upstream("app", ["10.0.0.1:80", "10.0.0.2:80"])
    want = "upstream app {\n    server 10.0.0.1:80;\n    server 10.0.0.2:80;\n}\n"
    assert got == want, repr(got)


def test_render_all_separates_blocks_with_blank_line():
    out = broken.render_all([("a.example", 80), ("b.example", 81)])
    assert out.count("server {") == 2
    assert "}\n\nserver {" in out
