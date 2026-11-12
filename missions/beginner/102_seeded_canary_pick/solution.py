# Mission 102 - Reproducible Canary Draw (solution)
# Chooses canary hosts for a rollout in a way that can be replayed from a seed.
import random


def pick_canaries(hosts, count, seed):
    pool = sorted(set(hosts))
    if count > len(pool):
        raise ValueError(f"asked for {count} canaries but only {len(pool)} hosts exist")
    rng = random.Random(seed)
    chosen = rng.sample(pool, count)
    return sorted(chosen)


def plan_waves(hosts, wave_size, seed):
    if wave_size < 1:
        raise ValueError("wave_size must be at least 1")
    remaining = sorted(set(hosts))
    waves = []
    while remaining:
        take = min(wave_size, len(remaining))
        wave = pick_canaries(remaining, take, seed + len(waves))
        waves.append(wave)
        remaining = [h for h in remaining if h not in wave]
    return waves


if __name__ == "__main__":
    fleet = [f"freight-{n:02d}" for n in range(1, 9)]
    print(pick_canaries(fleet, 2, seed=42))
    print(plan_waves(fleet, 3, seed=42))
