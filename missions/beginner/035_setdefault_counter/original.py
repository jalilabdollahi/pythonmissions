# Mission 035 - Count the Events
# Fix the bug.

def count_event(counts, event):
    """Increment counts[event] by 1, initializing if needed."""
    counts[event] += 1

if __name__ == "__main__":
    counts = {}
    count_event(counts, "deploy")
    count_event(counts, "deploy")
    count_event(counts, "rollback")
    print(counts)
