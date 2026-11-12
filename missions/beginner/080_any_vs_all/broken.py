# Mission 080 - Is the Cluster Healthy
# Classifies cache cluster state for the public status page.


def cluster_healthy(nodes):
    return any(n["up"] for n in nodes)


def cluster_degraded(nodes):
    return all(not n["up"] for n in nodes)


def cluster_down(nodes):
    return not any(n["up"] for n in nodes)


def status(nodes):
    if cluster_down(nodes):
        return "down"
    if cluster_degraded(nodes):
        return "degraded"
    return "healthy"


def down_names(nodes):
    return [n["name"] for n in nodes if not n["up"]]


def banner(nodes):
    state = status(nodes)
    if state == "degraded":
        return f"DEGRADED: {', '.join(down_names(nodes))}"
    return state.upper()


if __name__ == "__main__":
    cluster = [{"name": f"cache-{i}", "up": i != 3} for i in range(5)]
    print(banner(cluster))
