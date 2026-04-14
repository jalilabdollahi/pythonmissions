import pytest, sys
sys.path.insert(0, ".")
from broken import load_plugin, list_plugins

def test_load_valid_module():
    m = load_plugin("os.path")
    assert m is not None

def test_load_invalid_module():
    with pytest.raises(RuntimeError):
        load_plugin("definitely_not_a_real_module_xyz")

def test_list_plugins_skips_bad():
    result = list_plugins(["os.path", "nonexistent_xyz"])
    assert len(result) == 0  # os.path doesn't have execute/name/version
