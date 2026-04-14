# Mission 065 - Task Queue Processor
# Fix the 2 bugs in this script.
import heapq

class TaskQueue:
    def __init__(self):
        self._heap = []
        self._counter = 0

    def push(self, task, priority):
        # Higher priority number = processed first
        heapq.heappush(self._heap, (priority, self._counter, task))  # BUG 1: should negate priority
        self._counter += 1

    def pop(self):
        if not self._heap:
            raise IndexError("Queue is empty")
        _, _, task = heapq.heappop(self._heap)
        return task

    def peek(self):
        if not self._heap:
            return None
        return self._heap[1][2]  # BUG 2: index 0 is the top, not index 1
