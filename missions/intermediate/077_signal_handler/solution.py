# Mission 077 - Signal Handler
# Fixed solution
import signal

_shutdown_requested = False

def _handler(signum, frame):
    global _shutdown_requested
    _shutdown_requested = True
    print("Shutdown requested")

def setup_shutdown_handler():
    signal.signal(signal.SIGTERM, _handler)

def is_shutdown_requested():
    return _shutdown_requested
