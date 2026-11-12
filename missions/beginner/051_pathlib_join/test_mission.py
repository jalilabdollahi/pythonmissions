import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pathlib import Path

import broken


def test_release_dir_has_separator_between_root_and_project():
    got = broken.release_dir("billing", "1.4.2", "/srv/releases")
    assert got == Path("/srv/releases/billing/1.4.2"), "got %s" % got


def test_artifact_path_for_custom_root(tmp_path):
    got = broken.artifact_path("api", "2.0", "api.tar.gz", str(tmp_path))
    assert got == tmp_path / "api" / "2.0" / "api.tar.gz"


def test_checksum_sits_next_to_artifact():
    got = broken.checksum_path("api", "2.0", "api.tar.gz", "/data")
    assert got == Path("/data/api/2.0/api.tar.gz.sha256")


def test_latest_link_is_inside_project_directory():
    assert broken.latest_link("web", "/srv/releases") == Path("/srv/releases/web/latest")


def test_all_paths_returns_three_paths():
    paths = broken.all_paths("web", "9", "web.zip", "/r")
    assert [str(p) for p in paths] == ["/r/web/9/web.zip", "/r/web/9/web.zip.sha256", "/r/web/latest"]
