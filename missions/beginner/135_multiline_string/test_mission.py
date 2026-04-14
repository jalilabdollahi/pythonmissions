import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_has_newlines():
    from broken import build_script
    result = build_script(["cmd1", "cmd2", "cmd3"])
    assert "\n" in result

def test_correct_content():
    from broken import build_script
    result = build_script(["#!/bin/bash", "set -e"])
    assert "#!/bin/bash" in result and "set -e" in result

def test_no_extra_spaces():
    from broken import build_script
    result = build_script(["a", "b"])
    assert result == "a\nb"
