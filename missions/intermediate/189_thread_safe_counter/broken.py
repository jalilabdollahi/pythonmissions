# Mission 189 - Count On Me
# Thread-safe upload statistics shared by many request threads.
import threading


class UploadStats:
    def __init__(self):
        self._lock = threading.Lock()
        self.count = 0
        self.bytes = 0
        self.by_route = {}

    def record(self, route, nbytes):
        with threading.Lock():
            self.count += 1
            self.bytes += nbytes
            self.by_route[route] = self.by_route.get(route, 0) + 1

    def record_batch(self, route, sizes):
        with self._lock:
            for size in sizes:
                self.record(route, size)

    def snapshot(self):
        with self._lock:
            return {"count": self.count, "bytes": self.bytes, "by_route": self.by_route}


def main():
    stats = UploadStats()
    stats.record("/avatar", 2048)
    stats.record_batch("/docs", [10, 20, 30])
    print(stats.snapshot())


if __name__ == "__main__":
    main()
