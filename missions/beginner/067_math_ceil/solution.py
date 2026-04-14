# Mission 067 - Solution
import math

def replica_count(load, capacity):
    return math.ceil(load / capacity)

if __name__ == "__main__":
    print(replica_count(10, 3))
