# Mission 248 - Parallel Preflight Checks (solution)
# Run deployment checks concurrently: fail fast with clean cancellation, or settle them all.
import asyncio


class Outcome:
    def __init__(self, name, ok, value=None, error=None):
        self.name = name
        self.ok = ok
        self.value = value
        self.error = error

    def __repr__(self):
        detail = self.value if self.ok else repr(self.error)
        return f"Outcome({self.name!r}, ok={self.ok}, {detail!r})"


async def run_fail_fast(checks, timeout=None):
    """Run all `checks` (zero-argument coroutine functions) at once.

    Returns their results in submission order. The first exception cancels every
    other check, waits for them to finish unwinding and is then raised.
    On timeout, everything still running is cancelled and TimeoutError is raised.
    """
    tasks = [asyncio.ensure_future(check()) for check in checks]
    try:
        done, pending = await asyncio.wait(
            tasks, timeout=timeout, return_when=asyncio.FIRST_EXCEPTION
        )
        failed = [t for t in tasks if t in done and not t.cancelled() and t.exception()]
        if failed:
            raise failed[0].exception()
        if pending:
            raise asyncio.TimeoutError(f"{len(pending)} check(s) still running")
        return [t.result() for t in tasks]
    finally:
        for task in tasks:
            if not task.done():
                task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)


async def run_settled(named_checks):
    """Run every check to completion and report each one as an Outcome."""
    names = list(named_checks)
    results = await asyncio.gather(
        *(named_checks[name]() for name in names), return_exceptions=True
    )
    outcomes = []
    for name, result in zip(names, results):
        if isinstance(result, BaseException):
            outcomes.append(Outcome(name, False, error=result))
        else:
            outcomes.append(Outcome(name, True, value=result))
    return outcomes


def summarize(outcomes):
    failed = [o.name for o in outcomes if not o.ok]
    return {"passed": len(outcomes) - len(failed), "failed": failed, "healthy": not failed}


def format_report(outcomes):
    lines = []
    for outcome in outcomes:
        if outcome.ok:
            lines.append(f"PASS {outcome.name}: {outcome.value}")
        else:
            reason = type(outcome.error).__name__
            lines.append(f"FAIL {outcome.name}: {reason}")
    return "\n".join(lines)


async def preflight(checks, fail_fast=True, timeout=None):
    if fail_fast:
        return await run_fail_fast(list(checks.values()), timeout)
    return summarize(await run_settled(checks))
