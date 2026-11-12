import os
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def make_bundle(path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("libs/", "")
        zf.writestr("libs/driver.jar", b"J" * 100)
        zf.writestr("libs/Legacy-Driver.JAR", b"L" * 50)
        zf.writestr("libs/driver.jar.sha1", b"abc")
        zf.writestr("wheels/", "")
        zf.writestr("wheels/app-1.0-py3-none-any.whl", b"W" * 200)
        zf.writestr("README.txt", b"hello " * 100)
    return str(path)


def test_directory_entries_are_not_files(tmp_path):
    info = broken.inventory(make_bundle(tmp_path / "b.zip"))
    assert info["files"] == 5, "folder entries are not files"


def test_total_size_is_uncompressed(tmp_path):
    info = broken.inventory(make_bundle(tmp_path / "b.zip"))
    assert info["total_size"] == 100 + 50 + 3 + 200 + 600, "use file_size, not compress_size"


def test_extension_match_ignores_case(tmp_path):
    info = broken.inventory(make_bundle(tmp_path / "b.zip"))
    assert "libs/Legacy-Driver.JAR" in info["artifacts"]


def test_only_wheels_and_jars_are_artifacts(tmp_path):
    info = broken.inventory(make_bundle(tmp_path / "b.zip"))
    assert info["artifacts"] == [
        "libs/Legacy-Driver.JAR",
        "libs/driver.jar",
        "wheels/app-1.0-py3-none-any.whl",
    ]


def test_empty_bundle(tmp_path):
    path = tmp_path / "empty.zip"
    with zipfile.ZipFile(path, "w"):
        pass
    assert broken.inventory(str(path)) == {"artifacts": [], "files": 0, "total_size": 0}
