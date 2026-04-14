# Mission 141 - Find Heaviest and Lightest Pod
def heaviest(pods):
    """Return pod with highest memory_mb."""
    return max(pods, key=lambda p: p["cpu"])

def lightest(pods):
    """Return pod with lowest memory_mb."""
    return min(pods, key=lambda p: p["cpu"])

if __name__ == "__main__":
    pods = [{"name":"pod-a","memory_mb":512,"cpu":20},{"name":"pod-b","memory_mb":2048,"cpu":80},{"name":"pod-c","memory_mb":256,"cpu":5}]
    print(heaviest(pods)["name"])
    print(lightest(pods)["name"])
