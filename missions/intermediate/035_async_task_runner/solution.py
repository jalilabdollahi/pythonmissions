# Mission 035 - Async Task Runner
# Fixed solution
import asyncio

async def check_service(name, delay=0):
    await asyncio.sleep(delay)
    return {"service": name, "status": "ok"}

async def run_checks(services):
    """Run all checks concurrently and return results."""
    tasks = [check_service(s) for s in services]
    results = await asyncio.gather(*tasks)
    return results

def main(services):
    return asyncio.run(run_checks(services))
