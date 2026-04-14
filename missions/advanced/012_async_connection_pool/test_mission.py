import pytest, asyncio, sys
sys.path.insert(0, ".")
from broken import AsyncConnectionPool

def test_execute():
    pool = AsyncConnectionPool(3)
    result = asyncio.run(pool.execute("SELECT 1"))
    assert "SELECT 1" in result

def test_concurrent_execute():
    pool = AsyncConnectionPool(3)
    async def run():
        return await asyncio.gather(*[pool.execute(f"Q{i}") for i in range(3)])
    results = asyncio.run(run())
    assert len(results) == 3

def test_sem_size():
    pool = AsyncConnectionPool(3)
    assert pool._sem._value == 3
