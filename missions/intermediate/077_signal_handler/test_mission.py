import pytest, sys, signal, os
sys.path.insert(0, ".")
from broken import setup_shutdown_handler, is_shutdown_requested, _handler

def test_setup_does_not_crash():
    setup_shutdown_handler()

def test_handler_signature():
    import inspect
    params = inspect.signature(_handler).parameters
    assert len(params) == 2  # signum and frame

def test_shutdown_flag():
    import broken
    broken._shutdown_requested = False
    _handler(signal.SIGTERM, None)
    assert broken._shutdown_requested is True
