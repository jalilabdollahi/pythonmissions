import os
import struct
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def raw_frame(payload, seq, flags=0, version=1):
    return b"HX" + bytes([version, flags]) + struct.pack(">H", len(payload)) + struct.pack(">I", seq) + payload


def test_header_is_ten_bytes():
    assert broken.HEADER_SIZE == 10


def test_parse_hand_built_frame_big_endian():
    frame = raw_frame(b"x" * 258, seq=0x01020304)
    parsed = broken.parse_frame(frame)
    assert parsed["length"] == 258, "length is big-endian: bytes 01 02 mean 258"
    assert parsed["seq"] == 0x01020304
    assert parsed["payload"] == b"x" * 258


def test_flags_are_decoded_as_bits():
    parsed = broken.parse_frame(raw_frame(b"ab", seq=1, flags=0b10, version=3))
    assert parsed["version"] == 3
    assert parsed["flags"] == {"compressed": False, "encrypted": True}


def test_pack_and_parse_roundtrip():
    frame = broken.pack_frame(b"temp=21.5", seq=70000, compressed=True)
    parsed = broken.parse_frame(frame)
    assert parsed["payload"] == b"temp=21.5"
    assert parsed["seq"] == 70000
    assert parsed["flags"]["compressed"] is True


def test_oversized_payload_is_rejected_when_packing():
    with pytest.raises(ValueError, match="too large"):
        broken.pack_frame(b"x" * 70000, seq=1)
    assert len(broken.pack_frame(b"x" * 65535, seq=1)) == 10 + 65535


def test_truncated_payload_is_rejected():
    frame = broken.pack_frame(b"0123456789", seq=1)
    with pytest.raises(ValueError, match="truncated"):
        broken.parse_frame(frame[:-1])


def test_short_frames_and_bad_magic_are_rejected():
    with pytest.raises(ValueError):
        broken.parse_frame(b"HX\x01")
    with pytest.raises(ValueError, match="magic"):
        broken.parse_frame(b"ZZ" + raw_frame(b"a", 1)[2:])


def test_trailing_bytes_after_the_payload_are_ignored():
    frame = broken.pack_frame(b"abc", seq=5) + b"NEXTFRAME"
    assert broken.parse_frame(frame)["payload"] == b"abc"


def test_split_stream_returns_complete_frames_and_remainder():
    stream = broken.pack_frame(b"one", 1) + broken.pack_frame(b"two", 2)
    stream += broken.pack_frame(b"three", 3)[:-2]
    frames, rest = broken.split_stream(stream)
    assert [f["payload"] for f in frames] == [b"one", b"two"]
    assert len(rest) == broken.HEADER_SIZE + 3
