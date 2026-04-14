# Mission 019 - Structured Logger Setup
# Fix the 2 bugs in this script.
import logging

def setup_logger(name, log_file):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    logger = handler  # BUG 1: should be logger.addHandler(handler)
    return logger

def get_console_logger(name):
    logger = logging.getLogger(name)
    logging.basicConfig(level="DEBUG")  # BUG 2: should be logging.DEBUG (int), not string
    return logger
