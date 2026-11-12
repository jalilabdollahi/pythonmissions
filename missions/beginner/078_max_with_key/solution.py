# Mission 078 - Which Node Has Room (solution)
# Chooses nodes for jobs based on free memory.


def most_free_node(free_mb):
    if not free_mb:
        return None
    return max(free_mb, key=free_mb.get)


def least_free_node(free_mb):
    if not free_mb:
        return None
    return min(free_mb, key=free_mb.get)


def pick_for_job(free_mb, needed_mb):
    best = most_free_node(free_mb)
    if best is None:
        return None
    if free_mb[best] < needed_mb:
        return None
    return best


def summary(free_mb):
    if not free_mb:
        return "no nodes"
    best = most_free_node(free_mb)
    worst = least_free_node(free_mb)
    return f"most free: {best} ({free_mb[best]} MB), least free: {worst} ({free_mb[worst]} MB)"


if __name__ == "__main__":
    nodes = {"worker-1": 2048, "worker-2": 512, "worker-9": 128}
    print(summary(nodes))
    print(pick_for_job(nodes, 1024))
