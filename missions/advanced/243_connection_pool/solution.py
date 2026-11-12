# Mission 243 - Database Connection Pool (solution)
# Thread-safe bounded pool that hands out connections and takes them back.
import threading
import time
from contextlib import contextmanager


class PoolTimeout(Exception):
    pass


class ConnectionPool:
    def __init__(self, factory, max_size):
        self._factory = factory
        self._max_size = max_size
        self._idle = []
        self._in_use = set()
        self._created = 0
        self._cond = threading.Condition()
        self.waiters = 0

    def acquire(self, timeout=None):
        deadline = None if timeout is None else time.monotonic() + timeout
        with self._cond:
            while True:
                if self._idle:
                    conn = self._idle.pop()
                    self._in_use.add(conn)
                    return conn
                if self._created < self._max_size:
                    self._created += 1
                    break
                remaining = None if deadline is None else deadline - time.monotonic()
                if remaining is not None and remaining <= 0:
                    raise PoolTimeout("no connection available")
                self.waiters += 1
                try:
                    self._cond.wait(remaining)
                finally:
                    self.waiters -= 1
        try:
            conn = self._factory()
        except Exception:
            with self._cond:
                self._created -= 1
                self._cond.notify()
            raise
        with self._cond:
            self._in_use.add(conn)
        return conn

    def release(self, conn, broken=False):
        with self._cond:
            if conn not in self._in_use:
                return
            self._in_use.discard(conn)
            if broken:
                self._created -= 1
            else:
                self._idle.append(conn)
            self._cond.notify()
        if broken:
            self._close(conn)

    @staticmethod
    def _close(conn):
        close = getattr(conn, "close", None)
        if close:
            close()

    @contextmanager
    def connection(self, timeout=None):
        conn = self.acquire(timeout)
        broken = False
        try:
            yield conn
        except ConnectionError:
            broken = True
            raise
        finally:
            self.release(conn, broken=broken)

    def stats(self):
        with self._cond:
            return {"idle": len(self._idle), "in_use": len(self._in_use), "created": self._created}
