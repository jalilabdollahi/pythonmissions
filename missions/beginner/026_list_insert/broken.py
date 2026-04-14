# Mission 026 - Insert at the Front
# Fix the bug.

def push_priority(queue, task):
    """Insert task at the front of the queue."""
    queue.insert(len(queue), task)

if __name__ == "__main__":
    q = ["routine-deploy", "health-check"]
    push_priority(q, "hotfix-payment")
    print(q)
