import pytest, sys
sys.path.insert(0, ".")
from broken import APIVersionRouter

def test_version_routing():
    router = APIVersionRouter()
    router.register(1, lambda req: ({"version": 1}, 200))
    router.register(2, lambda req: ({"version": 2}, 200))
    result, code = router.route("application/vnd.api+json;version=2", {})
    assert code == 200
    assert result["version"] == 2

def test_default_fallback():
    router = APIVersionRouter()
    router.set_default(lambda req: ({"version": "default"}, 200))
    result, code = router.route(None, {})
    assert result["version"] == "default"

def test_no_handler():
    router = APIVersionRouter()
    result, code = router.route("version=99", {})
    assert code == 406
