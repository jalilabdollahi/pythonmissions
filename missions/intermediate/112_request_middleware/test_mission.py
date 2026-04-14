import pytest, sys
sys.path.insert(0, ".")
from broken import MiddlewareChain, auth_middleware, logging_middleware

def test_auth_passes():
    chain = MiddlewareChain()
    chain.use(auth_middleware)
    result = chain.handle({"token": "valid", "path": "/api"})
    assert result["status"] == 200
    assert result["request"].get("authenticated") is True

def test_auth_rejects():
    chain = MiddlewareChain()
    chain.use(auth_middleware)
    result = chain.handle({"path": "/api"})
    assert result["status"] == 401

def test_chain_order():
    order = []
    def m1(req, nxt): order.append(1); return nxt(req)
    def m2(req, nxt): order.append(2); return nxt(req)
    chain = MiddlewareChain()
    chain.use(m1)
    chain.use(m2)
    chain.handle({})
    assert order == [1, 2]
