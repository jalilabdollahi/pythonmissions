import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_starts_at_one():
    from broken import numbered_steps
    result = numbered_steps(["Pull image", "Run migrations"])
    assert result[0].startswith("1.")

def test_second_step():
    from broken import numbered_steps
    result = numbered_steps(["Pull image", "Run migrations"])
    assert result[1].startswith("2.")

def test_content_preserved():
    from broken import numbered_steps
    result = numbered_steps(["Pull image"])
    assert "Pull image" in result[0]
