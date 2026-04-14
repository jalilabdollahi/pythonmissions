# Mission 120 - Multiply All Replicas
from builtins import reduce

def total_capacity(replicas):
    """Return product of all replica counts."""
    return reduce(lambda a, b: a * b, replicas, 1)

if __name__ == "__main__":
    print(total_capacity([2, 3, 4]))
