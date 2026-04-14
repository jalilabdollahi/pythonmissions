# Mission 123 - Enforce the Health Check Interface
from abc import abstractmethod

class Monitor:
    @abstractmethod
    def check(self):
        """Run health check and return status."""

class BrokenMonitor(Monitor):
    pass

if __name__ == "__main__":
    try:
        m = BrokenMonitor()
        print("No error — abstract not enforced!")
    except TypeError as e:
        print(f"Caught: {e}")
