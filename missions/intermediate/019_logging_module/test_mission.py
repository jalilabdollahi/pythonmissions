import pytest
import sys
import logging
sys.path.insert(0, ".")
from broken import setup_logger, get_console_logger

def test_setup_logger(tmp_path):
    log_file = str(tmp_path / "test.log")
    logger = setup_logger("test_app", log_file)
    assert hasattr(logger, "info")
    logger.info("hello")
    with open(log_file) as f:
        content = f.read()
    assert "hello" in content

def test_console_logger():
    logger = get_console_logger("console_test")
    assert logger is not None
