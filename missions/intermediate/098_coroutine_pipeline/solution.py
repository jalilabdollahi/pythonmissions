# Mission 098 - Coroutine Pipeline
# Fixed solution
import asyncio

async def source(items):
    for item in items:
        await asyncio.sleep(0)
        yield item

async def transform(gen, fn):
    async for item in gen:
        yield fn(item)

async def pipeline_process(items, transforms):
    gen = source(items)
    for fn in transforms:
        gen = transform(gen, fn)
    results = []
    async for item in gen:
        results.append(item)
    return results
