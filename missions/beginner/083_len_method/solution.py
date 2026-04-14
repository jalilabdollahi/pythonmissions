# Mission 083 - Solution
class TaskQueue:
    def __init__(self):
        self._tasks = []

    def add(self, task):
        self._tasks.append(task)

    def pop(self):
        return self._tasks.pop(0) if self._tasks else None

    def __len__(self):
        return len(self._tasks)

if __name__ == "__main__":
    q = TaskQueue()
    q.add("deploy")
    q.add("test")
    print(len(q))
