# Mission 026 - Solution

def push_priority(queue, task):
    queue.insert(0, task)

if __name__ == "__main__":
    q = ["routine-deploy", "health-check"]
    push_priority(q, "hotfix-payment")
    print(q)
