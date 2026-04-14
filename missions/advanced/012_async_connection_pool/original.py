# Mission 012 (Advanced) - Async Connection Pool
# Fix the 2 bugs in this script.
import asyncio

class AsyncConnection:
    def __init__(self, id_): self.id = id_; self.in_use = False
    async def query(self, sql): return f"result:{sql}:{self.id}"

class AsyncConnectionPool:
    def __init__(self, size=5):
        self.size = size
        self._connections = [AsyncConnection(i) for i in range(size)]
        self._sem = asyncio.Semaphore(size * 2)  # BUG 1: should limit to `size`, not size*2
        self._lock = asyncio.Lock()

    async def acquire(self):
        await self._sem.acquire()
        async with self._lock:
            conn = next((c for c in self._connections if not c.in_use), None)
            if conn:
                conn.in_use = True
            return conn

    async def release(self, conn):
        if conn:
            conn.in_use = False
            # BUG 2: must release the semaphore
        pass

    async def execute(self, sql):
        conn = await self.acquire()
        try:
            return await conn.query(sql)
        finally:
            await self.release(conn)
