# Mission 156 - Batch Uploader
# Split a stream of ids into fixed-size batches for an API with a request limit.


def chunked(items, size):
    batch = []
    for item in items:
        batch.append(item)
        if len(batch) == size:
            yield batch
            batch.clear()


def push_in_batches(ids, send, size=25):
    sent = 0
    for batch in chunked(ids, size):
        send(batch)
        sent += len(batch)
    return sent
