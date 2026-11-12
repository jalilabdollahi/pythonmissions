import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import GENESIS, AuditLog, actors_between, record_hash, rechain, verify_chain


def make_log():
    log = AuditLog()
    log.append("ana", "grant:admin", 100)
    log.append("bo", "read:payroll", 200)
    log.append("cy", "delete:backup", 300)
    log.append("ana", "revoke:admin", 400)
    return log


def test_untouched_log_verifies():
    log = make_log()
    assert verify_chain(log.export()) == (True, None, "ok")
    assert log.records[0]["prev"] == GENESIS
    assert log.records[1]["prev"] == log.records[0]["hash"]


def test_editing_any_field_is_detected_at_that_record():
    for field, value in [("actor", "mallory"), ("action", "noop"), ("ts", 999)]:
        records = make_log().export()
        records[2][field] = value
        assert verify_chain(records) == (False, 2, "record modified"), field


def test_editing_the_first_record_is_detected():
    records = make_log().export()
    records[0]["actor"] = "mallory"
    ok, index, reason = verify_chain(records)
    assert (ok, index) == (False, 0), "the very first record is protected too"


def test_field_boundaries_cannot_be_shifted_to_forge_a_hash():
    a = record_hash(1, 5, "a|b", "c", GENESIS)
    b = record_hash(1, 5, "a", "b|c", GENESIS)
    assert a != b, "the encoding must be unambiguous"
    assert record_hash(1, 5, "x", "y", GENESIS) != record_hash(1, 5, "xy", "", GENESIS)


def test_swapping_records_breaks_the_links():
    records = make_log().export()
    records[1], records[2] = records[2], records[1]
    ok, index, _ = verify_chain(records)
    assert not ok and index == 1


def test_link_to_previous_record_is_checked_even_when_hashes_are_self_consistent():
    records = make_log().export()
    forged = dict(records[2])
    forged["prev"] = GENESIS
    forged["hash"] = record_hash(forged["seq"], forged["ts"], forged["actor"], forged["action"], GENESIS)
    records[2] = forged
    assert verify_chain(records) == (False, 2, "broken link")


def test_deleted_middle_record_is_a_sequence_or_link_failure():
    records = make_log().export()
    del records[1]
    ok, index, reason = verify_chain(records)
    assert not ok and index == 1


def test_truncation_and_rechaining_are_caught_by_the_external_anchor():
    log = make_log()
    anchor = log.head
    assert verify_chain(log.export(), anchor=anchor)[0]
    truncated = log.export()[:3]
    assert verify_chain(truncated) == (True, None, "ok"), "a prefix is a valid chain on its own"
    assert verify_chain(truncated, anchor=anchor) == (False, 3, "head does not match anchor")
    rewritten = log.export()
    rewritten[1]["action"] = "read:nothing"
    rechain(rewritten)
    assert verify_chain(rewritten)[0]
    assert not verify_chain(rewritten, anchor=anchor)[0]


def test_queries_refuse_to_run_on_a_corrupted_log():
    records = make_log().export()
    assert actors_between(records, 150, 350) == ["bo", "cy"]
    records[3]["actor"] = "eve"
    with pytest.raises(ValueError):
        actors_between(records, 0, 1000)
