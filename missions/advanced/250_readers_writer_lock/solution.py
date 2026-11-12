# Mission 250 - Config Store Read/Write Lock (solution)
# Readers-writer lock with writer preference, used to guard a shared in-memory config.
import threading
from contextlib import contextmanager


class RWLock:
    def __init__(self):
        self._cond = threading.Condition()
        self._readers = 0
        self._writer = False
        self.waiting_readers = 0
        self.waiting_writers = 0

    def acquire_read(self, timeout=None):
        with self._cond:
            self.waiting_readers += 1
            try:
                ok = self._cond.wait_for(
                    lambda: not self._writer and self.waiting_writers == 0, timeout
                )
            finally:
                self.waiting_readers -= 1
            if not ok:
                return False
            self._readers += 1
            return True

    def release_read(self):
        with self._cond:
            if self._readers <= 0:
                raise RuntimeError("release_read without a matching acquire_read")
            self._readers -= 1
            if self._readers == 0:
                self._cond.notify_all()

    def acquire_write(self, timeout=None):
        with self._cond:
            self.waiting_writers += 1
            try:
                ok = self._cond.wait_for(
                    lambda: not self._writer and self._readers == 0, timeout
                )
            finally:
                self.waiting_writers -= 1
            if not ok:
                self._cond.notify_all()
                return False
            self._writer = True
            return True

    def release_write(self):
        with self._cond:
            if not self._writer:
                raise RuntimeError("release_write without a matching acquire_write")
            self._writer = False
            self._cond.notify_all()

    @contextmanager
    def reading(self, timeout=None):
        if not self.acquire_read(timeout):
            raise TimeoutError("could not get the read lock")
        try:
            yield
        finally:
            self.release_read()

    @contextmanager
    def writing(self, timeout=None):
        if not self.acquire_write(timeout):
            raise TimeoutError("could not get the write lock")
        try:
            yield
        finally:
            self.release_write()


class ConfigStore:
    def __init__(self, initial=None):
        self._lock = RWLock()
        self._data = dict(initial or {})
        self.version = 0

    def get(self, key, default=None):
        with self._lock.reading():
            return self._data.get(key, default)

    def snapshot(self):
        with self._lock.reading():
            return self.version, dict(self._data)

    def update(self, changes):
        with self._lock.writing():
            self._data.update(changes)
            self.version += 1
            return self.version
