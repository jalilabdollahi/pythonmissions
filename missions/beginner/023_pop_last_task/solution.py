# Mission 023 - Solution

def pop_last(queue):
    return queue.pop()

if __name__ == "__main__":
    tasks = ["deploy-db", "deploy-api", "smoke-test"]
    print(pop_last(tasks))
    print(tasks)
