# Mission 035 - Solution

def count_event(counts, event):
    counts.setdefault(event, 0)
    counts[event] += 1

if __name__ == "__main__":
    counts = {}
    count_event(counts, "deploy")
    count_event(counts, "deploy")
    count_event(counts, "rollback")
    print(counts)
