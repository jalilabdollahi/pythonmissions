# Mission 023 - Pop the Last Task
# Fix the bug.

def pop_last(queue):
    """Remove and return the last item from the queue."""
    return queue.pop(0)

if __name__ == "__main__":
    tasks = ["deploy-db", "deploy-api", "smoke-test"]
    print(pop_last(tasks))
    print(tasks)
