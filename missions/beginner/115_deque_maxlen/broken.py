# Mission 115 - Rolling Log Window
from collections import deque

class LogWindow:
    def __init__(self):
        self._lines = deque()

    def add(self, line):
        self._lines.append(line)

    def lines(self):
        return list(self._lines)

if __name__ == "__main__":
    w = LogWindow()
    for i in range(150):
        w.add(f"line {i}")
    print(len(w.lines()))
