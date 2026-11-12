import os
import sys
import tarfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def build_tree(root):
    (root / "pages").mkdir(parents=True)
    (root / "pages" / "index.html").write_text("<h1>hi</h1>")
    (root / "pages" / "draft.swp").write_text("junk")
    (root / "config.yaml").write_text("a: 1")
    (root / "cache").mkdir()
    (root / "cache" / "tmp.bin").write_bytes(b"x" * 50)
    (root / "uploads").mkdir()
    (root / "uploads" / "a.tmp").write_text("partial")
    (root / "uploads" / "photo.jpg").write_text("jpeg")
    (root / "notes.tmp").write_text("keep me, only uploads/*.tmp is excluded")
    (root / "mycache.txt").write_text("keep me")
    return root


def backup(tmp_path, exclude=()):
    src = build_tree(tmp_path / "site")
    archive = tmp_path / "out.tgz"
    count = broken.make_backup(str(src), str(archive), exclude=exclude)
    return count, broken.list_backup(str(archive)), archive


def test_member_names_are_relative_to_the_source(tmp_path):
    _, names, _ = backup(tmp_path)
    assert "pages/index.html" in names, "names must not carry the absolute source path"
    assert all(not os.path.isabs(n) and not n.startswith("..") for n in names)


def test_excluded_directory_is_pruned_with_contents(tmp_path):
    _, names, _ = backup(tmp_path, ["cache"])
    assert "cache/tmp.bin" not in names, "skipping a directory skips everything inside it"
    assert "mycache.txt" in names


def test_name_patterns_are_applied_everywhere(tmp_path):
    _, names, _ = backup(tmp_path, ["*.swp"])
    assert "pages/draft.swp" not in names


def test_patterns_with_a_directory_match_relative_paths(tmp_path):
    _, names, _ = backup(tmp_path, ["uploads/*.tmp"])
    assert "uploads/a.tmp" not in names, "the pattern contains a slash so it needs the relative path"
    assert "notes.tmp" in names and "uploads/photo.jpg" in names


def test_full_listing_and_count(tmp_path):
    count, names, _ = backup(tmp_path, ["cache", "*.swp", "uploads/*.tmp"])
    assert names == ["config.yaml", "mycache.txt", "notes.tmp", "pages/index.html", "uploads/photo.jpg"]
    assert count == 5


def test_archive_roundtrip_content(tmp_path):
    _, _, archive = backup(tmp_path)
    with tarfile.open(str(archive)) as tar:
        data = tar.extractfile("config.yaml").read()
    assert data == b"a: 1"
