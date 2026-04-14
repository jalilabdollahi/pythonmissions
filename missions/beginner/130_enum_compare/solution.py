# Mission 130 - Solution
from enum import Enum

class ServiceState(Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    DEGRADED = "degraded"

def is_running(state):
    return state is ServiceState.RUNNING

if __name__ == "__main__":
    print(is_running(ServiceState.RUNNING))
    print(is_running(ServiceState.STOPPED))
