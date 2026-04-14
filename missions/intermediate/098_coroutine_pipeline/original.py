# Mission 098 - Coroutine Pipeline
# Fix the 2 bugs in this script.
import asyncio

async def source(items):
    """Async generator that yields items."""
    for item in items:
        await asyncio.sleep(0)
        return item  # BUG 1: should be yield, not return

async def transform(gen, fn):
    """Apply fn to each item from async generator."""
    async for item in gen:
        yield fn(item)

async def pipeline_process(items, transforms):
    """Apply a list of transform functions as a pipeline."""
    gen = source(items)
    for fn in transforms:
        gen = transform(gen, fn)
    results = []
    for item in gen:  # BUG 2: should be async for
        results.append(item)
    return results
