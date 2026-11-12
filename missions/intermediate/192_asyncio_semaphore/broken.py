# Mission 192 - Polite Downloader
# Download many artifacts concurrently while limiting parallelism with a semaphore.
import asyncio


async def fetch_all(urls, fetch, limit=3):
    if limit < 0:
        raise ValueError("limit must be at least 1")
    sem = asyncio.Semaphore(limit)

    async def one(url):
        sem = asyncio.Semaphore(limit)
        await sem.acquire()
        result = await fetch(url)
        sem.release()
        return result

    return await asyncio.gather(*(one(url) for url in urls), return_exceptions=True)


def split_results(results):
    values = [r for r in results if not isinstance(r, Exception)]
    errors = [r for r in results if isinstance(r, Exception)]
    return values, errors


async def _demo_fetch(url):
    await asyncio.sleep(0)
    if url.endswith("missing"):
        raise LookupError("404")
    return len(url)


def main():
    results = asyncio.run(fetch_all(["a.whl", "b.whl", "missing"], _demo_fetch, limit=2))
    values, errors = split_results(results)
    print("fetched:", values, "failed:", len(errors))


if __name__ == "__main__":
    main()
