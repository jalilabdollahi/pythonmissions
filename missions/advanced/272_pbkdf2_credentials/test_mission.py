import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import (
    CURRENT_ITERATIONS,
    SALT_BYTES,
    hash_password,
    login,
    needs_rehash,
    parse,
    policy_report,
    verify_password,
)

FAST = 1000  # keep the suite quick


def test_correct_password_verifies_and_wrong_one_does_not():
    stored = hash_password("s3cret!", iterations=FAST)
    assert verify_password("s3cret!", stored)
    assert not verify_password("s3cret?", stored)
    assert not verify_password("", stored)


def test_each_hash_gets_its_own_random_salt():
    a = hash_password("same-password", iterations=FAST)
    b = hash_password("same-password", iterations=FAST)
    assert a != b, "identical passwords must not produce identical stored values"
    assert len(parse(a)[1]) == SALT_BYTES


def test_hash_format_records_the_work_factor():
    stored = hash_password("pw", salt=b"0123456789abcdef", iterations=FAST)
    algorithm, iterations, _, _ = stored.split("$")
    assert (algorithm, iterations) == ("pbkdf2_sha256", str(FAST))
    assert stored == hash_password("pw", salt=b"0123456789abcdef", iterations=FAST), "fixed salt gives a fixed hash"


def test_old_hashes_verify_with_the_iterations_they_were_made_with():
    legacy = hash_password("hunter2", iterations=500)
    assert verify_password("hunter2", legacy), "verification must use the stored iteration count"
    assert not verify_password("hunter3", legacy)


def test_non_ascii_passwords_are_not_truncated():
    stored = hash_password("pässwörd-日本", iterations=FAST)
    assert verify_password("pässwörd-日本", stored)
    assert not verify_password("psswrd-", stored), "dropping non-ASCII characters weakens every such password"


@pytest.mark.parametrize(
    "garbage",
    ["", "plaintext", "md5$1$abc$def", "pbkdf2_sha256$x$AA==$AA==", "pbkdf2_sha256$10$!!!$AA==", "pbkdf2_sha256$0$AA==$AA==", None],
)
def test_malformed_stored_values_fail_closed(garbage):
    assert verify_password("anything", garbage) is False
    assert needs_rehash(garbage) is True


def test_login_upgrades_weak_hashes_only_after_a_successful_check():
    weak = hash_password("pw", iterations=600)
    assert login(weak, "wrong", target=FAST) == (False, None)
    ok, replacement = login(weak, "pw", target=FAST)
    assert ok and parse(replacement)[0] == FAST
    assert login(replacement, "pw", target=FAST) == (True, None)


def test_policy_report_lists_weak_and_broken_hashes():
    hashes = {
        "ana": hash_password("a", iterations=FAST),
        "bo": hash_password("b", iterations=10),
        "cy": "garbage",
    }
    assert policy_report(hashes, target=FAST) == ["bo", "cy"]
    assert CURRENT_ITERATIONS >= 100_000
