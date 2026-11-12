# Mission 220 - Wire Header Decoder (solution)
# Decode and encode binary sensor frames with the struct module.
import struct

MAGIC = b"HX"
HEADER_FORMAT = "!2sBBHI"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)


def pack_frame(payload, seq, version=1, compressed=False, encrypted=False):
    if len(payload) > 0xFFFF:
        raise ValueError("payload too large for a 2-byte length")
    flags = (1 if compressed else 0) | (2 if encrypted else 0)
    header = struct.pack("!2sBBHI", MAGIC, version, flags, len(payload), seq)
    return header + payload


def parse_frame(data):
    if len(data) < HEADER_SIZE:
        raise ValueError("frame too short for a header")
    magic, version, flags, length, seq = struct.unpack(HEADER_FORMAT, data[:HEADER_SIZE])
    if magic != MAGIC:
        raise ValueError(f"bad magic {magic!r}")
    payload = data[HEADER_SIZE:HEADER_SIZE + length]
    if len(payload) < length:
        raise ValueError(f"truncated payload: expected {length} bytes, got {len(payload)}")
    return {
        "version": version,
        "flags": {"compressed": bool(flags & 1), "encrypted": bool(flags & 2)},
        "length": length,
        "seq": seq,
        "payload": payload,
    }


def split_stream(buffer):
    frames = []
    while len(buffer) >= HEADER_SIZE:
        length = struct.unpack("!H", buffer[4:6])[0]
        total = HEADER_SIZE + length
        if len(buffer) < total:
            break
        frames.append(parse_frame(buffer[:total]))
        buffer = buffer[total:]
    return frames, buffer


if __name__ == "__main__":
    print(parse_frame(pack_frame(b"temp=21.5", seq=7)))
