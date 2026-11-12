import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


class FakeApi:
    def __init__(self, pages):
        self.pages = pages
        self.tokens = []

    def __call__(self, token):
        self.tokens.append(token)
        index = 0 if token is None else int(token)
        nxt = index + 1
        return {
            "items": self.pages[index],
            "next_token": str(nxt) if nxt < len(self.pages) else None,
        }


def servers(*names):
    return [{"name": n} for n in names]


def test_collects_items_from_all_pages_including_the_last():
    api = FakeApi([servers("a", "b"), servers("c", "d"), servers("e")])
    items, pages = broken.fetch_all(api)
    assert [s["name"] for s in items] == ["a", "b", "c", "d", "e"], "the last page has data too"
    assert pages == 3


def test_single_page_api():
    api = FakeApi([servers("only")])
    items, pages = broken.fetch_all(api)
    assert items == servers("only")
    assert pages == 1


def test_tokens_are_passed_in_order():
    api = FakeApi([servers("a"), servers("b"), servers("c")])
    broken.fetch_all(api)
    assert api.tokens == [None, "1", "2"]


def test_limit_stops_requesting_early():
    api = FakeApi([servers("a", "b"), servers("c", "d"), servers("e", "f")])
    items, pages = broken.fetch_all(api, limit=3)
    assert len(items) == 3, "result must be trimmed to the limit"
    assert pages == 2
    assert api.tokens == [None, "1"]


def test_limit_larger_than_data_returns_everything():
    api = FakeApi([servers("a"), servers("b")])
    items, pages = broken.fetch_all(api, limit=10)
    assert len(items) == 2 and pages == 2


def test_limit_zero_makes_no_requests():
    api = FakeApi([servers("a")])
    assert broken.fetch_all(api, limit=0) == ([], 0)
    assert api.tokens == [], "limit=0 means do not call the API"


def test_collect_names_uses_fetch_all():
    api = FakeApi([servers("x"), servers("y")])
    assert broken.collect_names(api) == ["x", "y"]
