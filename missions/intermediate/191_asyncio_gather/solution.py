# Mission 191 - Await All The Things (solution)
# Check many services concurrently with asyncio.gather.
import asyncio


async def check_service(name, probe):
    status = await probe(name)
    return status


async def check_all(names, probe):
    outcomes = await asyncio.gather(
        *(check_service(name, probe) for name in names), return_exceptions=True
    )
    report = {}
    for name, outcome in zip(names, outcomes):
        if isinstance(outcome, Exception):
            report[name] = "error: %s" % type(outcome).__name__
        else:
            report[name] = outcome
    return report


def count_ok(report):
    return sum(1 for status in report.values() if status == "ok")


async def _demo_probe(name):
    await asyncio.sleep(0)
    if name == "db":
        raise ConnectionError("down")
    return "ok"


def main():
    report = asyncio.run(check_all(["api", "db", "cache"], _demo_probe))
    print(report)
    print("ok:", count_ok(report))


if __name__ == "__main__":
    main()
