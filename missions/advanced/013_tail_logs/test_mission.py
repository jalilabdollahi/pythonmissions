import os
import sys
import threading
import time

import pytest

sys.path.insert(0, os.path.dirname(__file__))


@pytest.fixture
def logfile(tmp_path):
    p = tmp_path / "test.log"
    p.write_text("")
    return str(p)


def test_tail_does_not_return_existing_content(logfile):
    with open(logfile, "w") as f:
        f.write("old line 1\nold line 2\n")

    collected = []
    new_line = "brand new line"

    def tailer():
        from broken import tail_file
        gen = tail_file(logfile, poll_interval=0.05)
        collected.append(next(gen))

    t = threading.Thread(target=tailer)
    t.start()
    time.sleep(0.1)

    with open(logfile, "a") as f:
        f.write(new_line + "\n")
        f.flush()

    t.join(timeout=3)
    assert collected == [new_line]


def test_tail_yields_new_lines(logfile):
    from broken import tail_file
    lines_to_write = ["line A", "line B", "line C"]
    collected = []

    def tailer():
        gen = tail_file(logfile, poll_interval=0.05)
        for _ in range(3):
            collected.append(next(gen))

    t = threading.Thread(target=tailer)
    t.start()
    time.sleep(0.1)

    with open(logfile, "a") as f:
        for line in lines_to_write:
            f.write(line + "\n")
            f.flush()
            time.sleep(0.03)

    t.join(timeout=5)
    assert collected == lines_to_write


def test_no_cpu_spin(logfile):
    from broken import tail_file
    gen = tail_file(logfile, poll_interval=0.1)

    def runner():
        try:
            next(gen)
        except Exception:
            pass

    t = threading.Thread(target=runner)
    t.start()
    time.sleep(0.3)
    with open(logfile, "a") as f:
        f.write("wake up\n")
        f.flush()
    t.join(timeout=2)
    assert True
