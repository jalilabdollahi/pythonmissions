import pytest, sys, os
sys.path.insert(0, ".")
from broken import ConfigWatcher

def test_watches_directory(tmp_path):
    watcher = ConfigWatcher(str(tmp_path))
    assert watcher.watch_dir == str(tmp_path)

def test_callback_called(tmp_path):
    watcher = ConfigWatcher(str(tmp_path))
    seen = []
    watcher.on_change(lambda p: seen.append(p))
    (tmp_path / "config.yaml").write_text("env: prod")
    count = watcher.poll()
    assert count == 1
    assert len(seen) == 1
