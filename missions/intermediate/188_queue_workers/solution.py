# Mission 188 - Worker Shift Change (solution)
# Process jobs with a pool of queue workers that shut down cleanly.
import queue
import threading

SENTINEL = None


def _worker(q, handler, results, errors):
    while True:
        item = q.get()
        if item is SENTINEL:
            q.task_done()
            return
        index, payload = item
        try:
            results[index] = handler(payload)
        except Exception as exc:
            errors[index] = repr(exc)
        q.task_done()


def run_jobs(payloads, handler, workers=3, join_timeout=2.0):
    q = queue.Queue()
    results = {}
    errors = {}
    threads = [
        threading.Thread(target=_worker, args=(q, handler, results, errors), daemon=True)
        for _ in range(workers)
    ]
    for t in threads:
        t.start()
    for index, payload in enumerate(payloads):
        q.put((index, payload))
    for _ in threads:
        q.put(SENTINEL)
    for t in threads:
        t.join(timeout=join_timeout)
    return {
        "results": [results[i] for i in sorted(results)],
        "errors": errors,
        "stopped": not any(t.is_alive() for t in threads),
        "unfinished": q.unfinished_tasks,
    }
