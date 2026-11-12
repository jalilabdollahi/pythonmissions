import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def make_tree(root):
    files = ["top.log", "api/app.log", "api/logs/2024/old.log", "db/slow.log", "db/notes.txt",
             "api/releases/v1/deploy.yaml", "chart.yaml"]
    for rel in files:
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("x")
    (root / "db" / "legacy.yaml").mkdir()
    return root


def test_find_logs_reaches_every_depth(tmp_path):
    root = make_tree(tmp_path)
    assert broken.find_logs(str(root)) == ["api/app.log", "api/logs/2024/old.log", "db/slow.log", "top.log"], \
        "'**' only recurses when glob is called with recursive=True"


def test_find_logs_includes_top_level_file(tmp_path):
    root = make_tree(tmp_path)
    assert "top.log" in broken.find_logs(str(root))


def test_find_logs_ignores_other_extensions(tmp_path):
    root = make_tree(tmp_path)
    assert all(p.endswith(".log") for p in broken.find_logs(str(root)))


def test_find_manifests_skips_directories_named_like_files(tmp_path):
    root = make_tree(tmp_path)
    assert broken.find_manifests(str(root)) == ["api/releases/v1/deploy.yaml", "chart.yaml"], \
        "a directory called legacy.yaml is not a manifest"


def test_logs_per_service_counts_by_first_directory(tmp_path):
    root = make_tree(tmp_path)
    assert broken.logs_per_service(str(root)) == {"api": 2, "db": 1, "(root)": 1}


def test_empty_tree_has_no_results(tmp_path):
    assert broken.find_logs(str(tmp_path)) == []
    assert broken.logs_per_service(str(tmp_path)) == {}
