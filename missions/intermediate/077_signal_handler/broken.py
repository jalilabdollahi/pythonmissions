# Mission 077 - Signal Handler
# Fix the 2 bugs in this script.
import signal

_shutdown_requested = False

def _handler(frame):  # BUG 1: missing signum parameter
    global _shutdown_requested
    _shutdown_requested = True
    print("Shutdown requested")

def setup_shutdown_handler():
    signal.signal("SIGTERM", _handler)  # BUG 2: should be signal.SIGTERM (int constant)

def is_shutdown_requested():
    return _shutdown_requested
