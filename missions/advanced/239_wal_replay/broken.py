# Mission 239 - Crash-Safe Journal Replay
# Write-ahead log with CRC32 checksums, torn-tail detection and replay into a KV store.
import json
import struct
import zlib

HEADER = struct.Struct(">II")


def encode(record):
    payload = json.dumps(record, sort_keys=True).encode("utf-8")
    return HEADER.pack(len(payload), zlib.crc32(payload)) + payload


def read_records(path):
    with open(path, "rb") as handle:
        data = handle.read()
    records = []
    offset = 0
    while offset < len(data):
        if len(data) - offset < HEADER.size:
            return records, offset, "truncated"
        length, crc = HEADER.unpack_from(data, offset)
        start = offset + HEADER.size
        end = start + length
        payload = data[start:end]
        if zlib.crc32(payload) != crc:
            offset = end
            continue
        records.append(json.loads(payload.decode("utf-8")))
        offset = end
    return records, offset, "clean"


def apply_record(store, record):
    op = record["op"]
    if op == "set":
        store[record["key"]] = record["value"]
    elif op == "del":
        store.pop(record["key"], None)
    elif op == "incr":
        store[record["key"]] = store.get(record["key"], 0) + record["value"]
    else:
        raise ValueError(f"unknown op {op!r}")


def replay(path, store, after_seq=0):
    records, good_offset, status = read_records(path)
    if status == "corrupt":
        with open(path, "r+b") as handle:
            handle.truncate(good_offset)
    last_seq = after_seq
    for record in records:
        if record["seq"] >= after_seq:
            apply_record(store, record)
            last_seq = record["seq"]
    return status, last_seq


class WriteAheadLog:
    def __init__(self, path, start_seq=0):
        self.path = path
        self.seq = start_seq

    def append(self, op, key, value=None):
        self.seq += 1
        record = {"seq": self.seq, "op": op, "key": key, "value": value}
        with open(self.path, "ab") as handle:
            handle.write(encode(record))
        return self.seq
