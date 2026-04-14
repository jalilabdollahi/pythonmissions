import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_str_output():
    from broken import Alert
    a = Alert("CRITICAL", "Disk full")
    assert str(a) == "[CRITICAL] Disk full"

def test_print_uses_str(capsys):
    from broken import Alert
    a = Alert("WARN", "High CPU")
    print(a)
    out = capsys.readouterr().out.strip()
    assert out == "[WARN] High CPU"
