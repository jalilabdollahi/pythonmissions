import pytest, sys
sys.path.insert(0, ".")
from broken import render_template, render_nginx_config

def test_render_simple():
    result = render_template("hello {{ name }}", {"name": "world"})
    assert "world" in result

def test_nginx_config():
    result = render_nginx_config("api.example.com", port=443)
    assert "api.example.com" in result
    assert "443" in result
