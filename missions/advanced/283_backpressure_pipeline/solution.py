# Mission 283 - Conveyor Backpressure (solution)
# Bounded queues between pipeline stages with reject and drop-oldest overflow policies.
from collections import deque


class BoundedBuffer:
    def __init__(self, capacity, policy):
        if policy not in ("reject", "drop_oldest"):
            raise ValueError(f"unknown policy {policy!r}")
        self.capacity = capacity
        self.policy = policy
        self.items = deque()
        self.accepted = 0
        self.rejected = 0
        self.dropped = 0

    def offer(self, item):
        """Try to enqueue. Returns True when the item is now in the buffer."""
        if len(self.items) >= self.capacity:
            if self.policy == "reject":
                self.rejected += 1
                return False
            self.dropped += 1
            self.items.popleft()
        self.items.append(item)
        self.accepted += 1
        return True

    def peek(self):
        return self.items[0]

    def pop(self):
        return self.items.popleft()

    def __len__(self):
        return len(self.items)


class Stage:
    def __init__(self, name, fn, capacity, policy="reject"):
        self.name = name
        self.fn = fn
        self.buffer = BoundedBuffer(capacity, policy)


class Pipeline:
    def __init__(self, stages):
        self.stages = stages
        self.output = []

    def push(self, item):
        return self.stages[0].buffer.offer(item)

    def step(self):
        """Advance every stage by at most one item, last stage first."""
        for index in range(len(self.stages) - 1, -1, -1):
            stage = self.stages[index]
            if not len(stage.buffer):
                continue
            result = stage.fn(stage.buffer.peek())
            if index == len(self.stages) - 1:
                stage.buffer.pop()
                self.output.append(result)
            elif self.stages[index + 1].buffer.offer(result):
                stage.buffer.pop()

    def drain(self, max_steps=1000):
        for _ in range(max_steps):
            if not any(len(s.buffer) for s in self.stages):
                break
            self.step()
        return self.output

    def stats(self):
        return {
            s.name: {
                "queued": len(s.buffer),
                "accepted": s.buffer.accepted,
                "rejected": s.buffer.rejected,
                "dropped": s.buffer.dropped,
            }
            for s in self.stages
        }
