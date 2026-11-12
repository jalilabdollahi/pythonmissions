import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def make_tree(root):
    (root / "pkg" / "__pycache__").mkdir(parents=True)
    (root / ".git").mkdir()
    (root / "pkg" / "app.py").write_text("print('v1')\n")
    (root / "pkg" / "util.py").write_text("X = 1\n")
    (root / "pkg" / "app.pyc").write_bytes(b"\x00\x01")
    (root / "pkg" / "__pycache__" / "app.cpython-310.pyc").write_bytes(b"\x00")
    (root / ".git" / "HEAD").write_text("ref: refs/heads/main\n")
    (root / "run.log").write_text("noise\n")
    (root / "README.md").write_text("hi\n")
    return root


def test_manifest_lists_nested_files_as_relative_paths(tmp_path):
    make_tree(tmp_path / "src")
    result = broken.stage_release(tmp_path / "src", tmp_path / "stage")
    assert result == ["README.md", "pkg/app.py", "pkg/util.py"]


def test_compiled_files_are_left_out(tmp_path):
    make_tree(tmp_path / "src")
    broken.stage_release(tmp_path / "src", tmp_path / "stage")
    assert not (tmp_path / "stage" / "pkg" / "app.pyc").exists(), "ignore patterns are globs: use *.pyc"
    assert not (tmp_path / "stage" / ".git").exists()
    assert not (tmp_path / "stage" / "run.log").exists()


def test_staging_twice_refreshes_files(tmp_path):
    src = make_tree(tmp_path / "src")
    broken.stage_release(src, tmp_path / "stage")
    (src / "pkg" / "app.py").write_text("print('v2')\n")
    result = broken.stage_release(src, tmp_path / "stage")
    assert (tmp_path / "stage" / "pkg" / "app.py").read_text() == "print('v2')\n"
    assert "pkg/app.py" in result


def test_extra_ignore_patterns(tmp_path):
    src = make_tree(tmp_path / "src")
    (src / "secrets.env").write_text("TOKEN=1\n")
    result = broken.stage_release(src, tmp_path / "stage", extra_ignore=("*.env", "README*"))
    assert result == ["pkg/app.py", "pkg/util.py"]


def test_is_clean_detects_junk(tmp_path):
    src = make_tree(tmp_path / "src")
    broken.stage_release(src, tmp_path / "stage")
    assert broken.is_clean(tmp_path / "stage")
    assert not broken.is_clean(src)


def test_skipped_lists_what_was_filtered_out(tmp_path):
    src = make_tree(tmp_path / "src")
    broken.stage_release(src, tmp_path / "stage")
    assert broken.skipped(src, tmp_path / "stage") == [
        ".git/HEAD",
        "pkg/__pycache__/app.cpython-310.pyc",
        "pkg/app.pyc",
        "run.log",
    ]


def test_by_extension_counts_staged_files(tmp_path):
    src = make_tree(tmp_path / "src")
    broken.stage_release(src, tmp_path / "stage")
    assert broken.by_extension(tmp_path / "stage") == {".md": 1, ".py": 2}


def test_total_size_counts_bytes(tmp_path):
    src = make_tree(tmp_path / "src")
    broken.stage_release(src, tmp_path / "stage")
    expected = len("print('v1')\n") + len("X = 1\n") + len("hi\n")
    assert broken.total_size(tmp_path / "stage") == expected
