import pytest, sys
sys.path.insert(0, ".")
from broken import total_pages, fetch_all_pages
from unittest.mock import MagicMock

def test_total_pages_exact():
    assert total_pages(100, 10) == 10

def test_total_pages_partial():
    assert total_pages(101, 10) == 11

def test_fetch_all_pages():
    sess = MagicMock()
    pages = [
        {"items": [1, 2, 3], "total": 5},
        {"items": [4, 5], "total": 5},
    ]
    resp = MagicMock()
    resp.json.side_effect = pages
    sess.get.return_value = resp
    result = fetch_all_pages(sess, "http://api.example.com/items", per_page=3)
    assert result == [1, 2, 3, 4, 5]
