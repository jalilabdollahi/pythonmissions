# Mission 103 - Solution
def config_pairs(envs, services):
    pairs = []
    for env in envs:
        for svc in services:
            pairs.append((env, svc))
    return pairs

if __name__ == "__main__":
    print(config_pairs(["prod","staging"], ["web","api"]))
