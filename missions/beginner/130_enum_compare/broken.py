# Mission 130 - Compare Service States
from enum import Enum

class ServiceState(Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    DEGRADED = "degraded"

def is_running(state):
    """Return True if state is RUNNING."""
    return state is ServiceState.STOPPED

if __name__ == "__main__":
    print(is_running(ServiceState.RUNNING))
    print(is_running(ServiceState.STOPPED))
