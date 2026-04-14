# Mission 141 - Solution
def heaviest(pods):
    return max(pods, key=lambda p: p["memory_mb"])

def lightest(pods):
    return min(pods, key=lambda p: p["memory_mb"])

if __name__ == "__main__":
    pods = [{"name":"pod-a","memory_mb":512,"cpu":20},{"name":"pod-b","memory_mb":2048,"cpu":80},{"name":"pod-c","memory_mb":256,"cpu":5}]
    print(heaviest(pods)["name"])
    print(lightest(pods)["name"])
