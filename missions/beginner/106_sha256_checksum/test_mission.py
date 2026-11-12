import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import hashlib

from broken import file_sha256, verify_checksum, describe


def make_file(tmp_path, data, name="image.bin"):
    path = tmp_path / name
    path.write_bytes(data)
    return str(path)


def test_known_hash_of_text_bytes(tmp_path):
    path = make_file(tmp_path, b"hello")
    assert file_sha256(path) == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"


def test_hash_is_64_char_hex_string(tmp_path):
    result = file_sha256(make_file(tmp_path, b"abc"))
    assert isinstance(result, str) and len(result) == 64, "use hexdigest() for the printable form"


def test_binary_file_with_invalid_utf8(tmp_path):
    data = bytes(range(256)) * 20
    path = make_file(tmp_path, data)
    assert file_sha256(path) == hashlib.sha256(data).hexdigest(), "hash raw bytes: open in binary mode"


def test_windows_newlines_are_not_altered(tmp_path):
    data = b"line1\r\nline2\r\n"
    assert file_sha256(make_file(tmp_path, data)) == hashlib.sha256(data).hexdigest()


def test_file_larger_than_one_chunk(tmp_path):
    data = b"x" * 50000
    assert file_sha256(make_file(tmp_path, data)) == hashlib.sha256(data).hexdigest()


def test_verify_checksum_ignores_case_and_spaces(tmp_path):
    path = make_file(tmp_path, b"hello")
    good = "2CF24DBA5FB0A30E26E83B2AC5B9E29E1B161E5C1FA7425E73043362938B9824 "
    assert verify_checksum(path, good) is True
    assert verify_checksum(path, "0" * 64) is False


def test_describe_shows_hex(tmp_path):
    assert describe(make_file(tmp_path, b"hello")).endswith("sha256:2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824")
