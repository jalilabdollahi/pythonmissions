import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_three_letter_extension():
    assert broken.extension("app.JAR") == "jar"


def test_longer_extension_is_complete():
    assert broken.extension("index.html") == "html", "extensions are not always three characters"


def test_short_extension_has_no_dot_or_neighbours():
    assert broken.extension("notes.md") == "md"


def test_no_extension_gives_empty_string():
    assert broken.extension("Makefile") == ""


def test_only_last_extension_counts():
    assert broken.extension("bundle.tar.gz") == "gz"


def test_grouping_and_counts():
    names = ["b.json", "a.json", "run.py", "Makefile"]
    assert broken.group_by_extension(names) == {"json": ["a.json", "b.json"], "py": ["run.py"], "": ["Makefile"]}
    assert broken.count_by_extension(names)["json"] == 2


def test_upload_folders():
    assert broken.folders(["x.yaml", "Dockerfile"]) == ["misc", "yaml"]
