# Mission 103 - Build the Config Matrix
def config_pairs(envs, services):
    """Return all (env, service) combinations."""
    pairs = []
    for i in envs:
        for i in services:
            pairs.append((i, i))
    return pairs

if __name__ == "__main__":
    print(config_pairs(["prod","staging"], ["web","api"]))
