# Mission 205 - Crash Log Tail (solution)
# Keep only the most recent log lines of a crashing worker.
from collections import deque


class LogTail:
    def __init__(self, capacity):
        if capacity < 1:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._lines = deque(maxlen=capacity)

    def add(self, line):
        self._lines.append(line.rstrip("\n"))

    def add_chunk(self, text):
        for line in text.splitlines():
            self.add(line)

    def tail(self, n):
        if n <= 0:
            return []
        return list(self._lines)[-n:]

    def last(self):
        return self._lines[-1] if self._lines else None

    def clear(self):
        self._lines.clear()

    def ticket_text(self):
        return "\n".join(self._lines)

    def __len__(self):
        return len(self._lines)


def attach_to_ticket(tail, header, n=50):
    body = "\n".join(tail.tail(n))
    return f"{header}\n--- last {min(n, len(tail))} lines ---\n{body}"


if __name__ == "__main__":
    buf = LogTail(3)
    buf.add_chunk("boot\nready\nserving\ncrash\n")
    print(attach_to_ticket(buf, "worker-7 died", n=2))
