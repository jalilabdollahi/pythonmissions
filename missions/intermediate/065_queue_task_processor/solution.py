# Mission 065 - Task Queue Processor
# Fixed solution
import heapq

class TaskQueue:
    def __init__(self):
        self._heap = []
        self._counter = 0

    def push(self, task, priority):
        heapq.heappush(self._heap, (-priority, self._counter, task))
        self._counter += 1

    def pop(self):
        if not self._heap:
            raise IndexError("Queue is empty")
        _, _, task = heapq.heappop(self._heap)
        return task

    def peek(self):
        if not self._heap:
            return None
        return self._heap[0][2]
