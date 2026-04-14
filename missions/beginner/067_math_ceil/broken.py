# Mission 067 - Round Up the Replica Count
import math

def replica_count(load, capacity):
    """Return minimum replicas needed (always round up)."""
    return math.floor(load / capacity)

if __name__ == "__main__":
    print(replica_count(10, 3))
