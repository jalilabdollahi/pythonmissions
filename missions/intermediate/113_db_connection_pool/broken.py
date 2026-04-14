# Mission 113 - Database Connection Pool
# Fix the 2 bugs in this script.
import threading

class FakeConnection:
    def __init__(self, id_): self.id = id_; self.closed = False
    def close(self): self.closed = True
    def query(self, sql): return f"result of {sql}"

class ConnectionPool:
    def __init__(self, max_size=5):
        self.max_size = max_size
        self._pool = [FakeConnection(i) for i in range(max_size)]
        self._lock = threading.Lock()

    def acquire(self):
        with self._lock:
            if self._pool:
                return self._pool.pop()
            return FakeConnection(999)  # BUG 1: should raise RuntimeError when exhausted

    def release(self, conn):
        with self._lock:
            pass  # BUG 2: should append conn back to self._pool

    def execute(self, sql):
        conn = self.acquire()
        try:
            return conn.query(sql)
        finally:
            self.release(conn)
