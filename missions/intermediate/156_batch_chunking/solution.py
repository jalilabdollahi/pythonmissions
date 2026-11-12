# Mission 156 - Batch Uploader (solution)
# Split a stream of ids into fixed-size batches for an API with a request limit.


def chunked(items, size):
    if size < 1:
        raise ValueError("size must be at least 1")
    batch = []
    for item in items:
        batch.append(item)
        if len(batch) == size:
            yield batch
            batch = []


    if batch:
        yield batch


def push_in_batches(ids, send, size=25):
    sent = 0
    for batch in chunked(ids, size):
        send(batch)
        sent += len(batch)
    return sent
