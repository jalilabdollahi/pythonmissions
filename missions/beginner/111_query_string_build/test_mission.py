import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import build_query, search_url, logs_link, logs_home


def test_plain_values_pass_through():
    assert build_query({"env": "prod", "tier": "web"}) == "env=prod&tier=web"


def test_spaces_become_plus():
    assert build_query({"q": "disk full"}) == "q=disk+full"


def test_ampersand_in_value_is_escaped():
    assert build_query({"region": "prod&eu"}) == "region=prod%26eu", "an unescaped & would start a new parameter"


def test_equals_and_hash_are_escaped():
    assert build_query({"filter": "a=b#c"}) == "filter=a%3Db%23c"


def test_non_ascii_is_utf8_percent_encoded():
    assert build_query({"name": "caf\u00e9"}) == "name=caf%C3%A9"


def test_search_url_without_params_has_no_question_mark():
    assert search_url("https://x.example/logs", {}) == "https://x.example/logs"


def test_logs_links():
    assert logs_link("api gateway", "slow & late") == "https://status.orchard.example/logs?service=api+gateway&q=slow+%26+late"
    assert logs_home() == "https://status.orchard.example/logs"
