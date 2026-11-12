# Mission 244 - Render Slot Pool
# asyncio slot pool with direct hand-off to waiters; slots must survive cancellation.
import asyncio
from collections import deque


class SlotPool:
    def __init__(self, capacity):
        self.capacity = capacity
        self.in_use = 0
        self._waiters = deque()

    async def acquire(self):
        if self.in_use < self.capacity and not self._waiters:
            self.in_use += 1
            return
        fut = asyncio.get_running_loop().create_future()
        self._waiters.append(fut)
        try:
            await fut
        except asyncio.CancelledError:
            if fut.done() and not fut.cancelled():
                pass
            else:
                try:
                    self._waiters.remove(fut)
                except ValueError:
                    pass
            raise

    def _next_live_waiter(self):
        while self._waiters:
            fut = self._waiters.popleft()
            return fut
        return None

    def try_acquire(self):
        if self.in_use < self.capacity and not self._waiters:
            self.in_use += 1
            return True
        return False

    def release(self):
        fut = self._next_live_waiter()
        if fut is not None:
            fut.set_result(None)
            return
        if self.in_use <= 0:
            raise RuntimeError("release without matching acquire")
        self.in_use -= 1

    def grow(self, extra):
        self.capacity += extra
        while self.in_use < self.capacity:
            fut = self._next_live_waiter()
            if fut is None:
                break
            self.in_use += 1
            fut.set_result(None)

    def stats(self):
        return {"capacity": self.capacity, "in_use": self.in_use, "waiting": self.waiting()}

    def waiting(self):
        return sum(1 for fut in self._waiters if not fut.done())

    async def run(self, job):
        await self.acquire()
        try:
            result = await job()
        except Exception:
            self.release()
            raise
        self.release()
        return result


async def render_all(pool, jobs):
    tasks = [asyncio.ensure_future(pool.run(job)) for job in jobs]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
