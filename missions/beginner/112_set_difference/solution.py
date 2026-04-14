# Mission 112 - Solution
def new_alerts(previous, current):
    return current.difference(previous)

if __name__ == "__main__":
    prev = {"disk-full", "high-cpu"}
    curr = {"disk-full", "oom", "network-down"}
    print(new_alerts(prev, curr))
