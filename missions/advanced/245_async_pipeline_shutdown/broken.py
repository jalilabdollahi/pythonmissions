# Mission 245 - Webhook Delivery Pipeline
# asyncio producer/consumer pipeline that must shut down cleanly.
import asyncio

_STOP = object()


class Report:
    def __init__(self):
        self.delivered = []
        self.failed = []

    def summary(self):
        return {"delivered": len(self.delivered), "failed": len(self.failed)}


class DeliveryPipeline:
    def __init__(self, deliver, workers=3, maxsize=4):
        self._deliver = deliver
        self._workers = workers
        self._maxsize = maxsize
        self.report = Report()
        self.active_tasks = []

    async def _worker(self, queue):
        while True:
            item = await queue.get()
            if item is _STOP:
                return
            try:
                if item is _STOP:
                    return
                try:
                    result = await self._deliver(item)
                except Exception as exc:
                    self.report.failed.append((item, type(exc).__name__))
                    return
                self.report.delivered.append(result)
            finally:
                queue.task_done()

    async def _produce(self, source, queue):
        try:
            async for item in source:
                await queue.put(item)
        except asyncio.CancelledError:
            raise
        else:
            for _ in range(1):
                await queue.put(_STOP)

    async def run(self, source):
        queue = asyncio.Queue(maxsize=self._maxsize)
        workers = [asyncio.ensure_future(self._worker(queue)) for _ in range(self._workers)]
        producer = asyncio.ensure_future(self._produce(source, queue))
        self.active_tasks = workers + [producer]
        source_error = None
        try:
            try:
                await producer
            except Exception as exc:
                source_error = exc
            await queue.join()
            await asyncio.gather(*workers)
        finally:
            for task in self.active_tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*self.active_tasks, return_exceptions=True)
        if source_error is not None:
            raise source_error
        return self.report


async def from_list(items):
    for item in items:
        yield item
