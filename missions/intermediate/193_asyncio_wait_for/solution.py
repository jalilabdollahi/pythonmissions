# Mission 193 - Deadline Diplomacy (solution)
# Give every async probe its own timeout and summarise the worst outcome.
import asyncio

RANK = {"ok": 0, "timeout": 1, "error": 2}


async def run_probe(name, probe, timeout_ms):
    try:
        value = await asyncio.wait_for(probe(name), timeout_ms / 1000)
        return {"name": name, "status": "ok", "value": value}
    except asyncio.TimeoutError:
        return {"name": name, "status": "timeout", "value": None}
    except Exception as exc:
        return {"name": name, "status": "error", "value": type(exc).__name__}


async def run_all(names, probe, timeout_ms=100):
    return list(await asyncio.gather(*(run_probe(n, probe, timeout_ms) for n in names)))


def worst(results):
    if not results:
        return "ok"
    return max(results, key=lambda r: RANK[r["status"]])["status"]


async def _demo_probe(name):
    if name == "slow":
        await asyncio.sleep(1)
    return "200 " + name


def main():
    results = asyncio.run(run_all(["fast", "slow"], _demo_probe, timeout_ms=50))
    for result in results:
        print(result)
    print("worst:", worst(results))


if __name__ == "__main__":
    main()
