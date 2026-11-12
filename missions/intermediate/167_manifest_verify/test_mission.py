import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken

DATA = b"0123456789abcdef" * 5


def sha(data):
    return hashlib.sha256(data).hexdigest()


def test_digest_of_small_file(tmp_path):
    path = tmp_path / "small.bin"
    path.write_bytes(b"abc")
    assert broken.file_digest(str(path), 1024) == sha(b"abc")


def test_digest_of_file_larger_than_one_chunk(tmp_path):
    path = tmp_path / "big.bin"
    path.write_bytes(DATA)
    assert broken.file_digest(str(path), 7) == sha(DATA), "all chunks must feed one running hash"


def test_digest_of_empty_file(tmp_path):
    path = tmp_path / "empty"
    path.write_bytes(b"")
    assert broken.file_digest(str(path)) == sha(b"")


def test_manifest_parsing_skips_blank_lines():
    text = f"{sha(b'a')}  one.txt\n\n{sha(b'b')}  dir/two file.txt\n"
    assert broken.parse_manifest(text) == [(sha(b"a"), "one.txt"), (sha(b"b"), "dir/two file.txt")]


def test_verify_reports_ok_and_mismatch(tmp_path):
    (tmp_path / "good.bin").write_bytes(DATA)
    (tmp_path / "bad.bin").write_bytes(DATA + b"!")
    manifest = f"{sha(DATA)}  good.bin\n{sha(DATA)}  bad.bin\n"
    report = broken.verify_manifest(str(tmp_path), manifest, chunk_size=10)
    assert report == {"ok": ["good.bin"], "mismatch": ["bad.bin"], "missing": []}


def test_uppercase_hex_in_manifest_is_accepted(tmp_path):
    (tmp_path / "a").write_bytes(b"payload")
    manifest = f"{sha(b'payload').upper()}  a\n"
    assert broken.verify_manifest(str(tmp_path), manifest)["ok"] == ["a"]


def test_missing_file_is_reported_without_aborting(tmp_path):
    (tmp_path / "present").write_bytes(b"1")
    manifest = f"{sha(b'x')}  gone.bin\n{sha(b'1')}  present\n"
    report = broken.verify_manifest(str(tmp_path), manifest)
    assert report == {"ok": ["present"], "mismatch": [], "missing": ["gone.bin"]}
