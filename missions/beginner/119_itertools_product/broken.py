# Mission 119 - Generate All Deploy Combos
from itertools import product

def all_combos(envs, services, regions):
    """Return cartesian product of envs, services, regions."""
    return list(product([envs, services, regions]))

if __name__ == "__main__":
    print(all_combos(["prod","staging"],["web","api"],["us","eu"]))
