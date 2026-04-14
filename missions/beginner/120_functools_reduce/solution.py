# Mission 120 - Solution
from functools import reduce

def total_capacity(replicas):
    return reduce(lambda a, b: a * b, replicas, 1)

if __name__ == "__main__":
    print(total_capacity([2, 3, 4]))
