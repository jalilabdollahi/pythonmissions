import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import WriteAheadLog, read_records, replay


def make_log(tmp_path, count=3):
    path = str(tmp_path / "agent.wal")
    wal = WriteAheadLog(path)
    wal.append("set", "mode", "eco")
    wal.append("incr", "boots", 1)
    wal.append("incr", "boots", 1)
    for i in range(count - 3):
        wal.append("set", f"k{i}", i)
    return path, wal


def test_clean_log_replays_every_record(tmp_path):
    path, _ = make_log(tmp_path)
    store = {}
    status, last = replay(path, store)
    assert (status, last) == ("clean", 3)
    assert store == {"mode": "eco", "boots": 2}


def test_delete_removes_key_and_missing_delete_is_harmless(tmp_path):
    path, wal = make_log(tmp_path)
    wal.append("del", "mode")
    wal.append("del", "never-existed")
    store = {}
    replay(path, store)
    assert store == {"boots": 2}


def test_torn_tail_is_reported_as_truncated_and_prefix_survives(tmp_path):
    path, _ = make_log(tmp_path)
    size = os.path.getsize(path)
    with open(path, "r+b") as f:
        f.truncate(size - 5)
    records, good, status = read_records(path)
    assert status == "truncated", "a half-written last record is expected after a crash"
    assert [r["seq"] for r in records] == [1, 2]
    assert good < size - 5


def test_replay_repairs_the_file_so_new_appends_are_durable(tmp_path):
    path, _ = make_log(tmp_path)
    with open(path, "r+b") as f:
        f.truncate(os.path.getsize(path) - 3)
    store = {}
    status, last = replay(path, store)
    assert status == "truncated" and last == 2
    wal = WriteAheadLog(path, start_seq=last)
    wal.append("set", "mode", "turbo")
    fresh = {}
    assert replay(path, fresh)[0] == "clean", "garbage tail must have been cut off"
    assert fresh == {"mode": "turbo", "boots": 1}


def test_checksum_mismatch_stops_scanning(tmp_path):
    path, _ = make_log(tmp_path)
    records, good, _ = read_records(path)
    first_len = len(open(path, "rb").read()) // 3
    raw = bytearray(open(path, "rb").read())
    raw[first_len + 12] ^= 0xFF
    open(path, "wb").write(bytes(raw))
    records, good, status = read_records(path)
    assert status == "corrupt"
    assert [r["seq"] for r in records] == [1], "nothing after the first bad record can be trusted"


def test_records_covered_by_the_checkpoint_are_not_reapplied(tmp_path):
    path, _ = make_log(tmp_path)
    store = {"mode": "eco", "boots": 2}
    status, last = replay(path, store, after_seq=3)
    assert store["boots"] == 2, "incr records up to seq 3 are already in the snapshot"
    assert last == 3


def test_partial_checkpoint_applies_only_newer_increments(tmp_path):
    path, _ = make_log(tmp_path)
    store = {"mode": "eco", "boots": 1}
    replay(path, store, after_seq=2)
    assert store["boots"] == 2
