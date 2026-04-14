# Mission 035 - Async Task Runner
# Fix the 2 bugs in this script.
import asyncio

async def check_service(name, delay=0):
    await asyncio.sleep(delay)
    return {"service": name, "status": "ok"}

async def run_checks(services):
    """Run all checks concurrently and return results."""
    tasks = [check_service(s) for s in services]  # BUG 1: not awaited coroutines
    results = await asyncio.gather(tasks)  # BUG 2: gather takes *args not a list
    return results

def main(services):
    return asyncio.run(run_checks(services))
