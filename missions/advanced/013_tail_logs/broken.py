# Mission 13 - Tail the Log File
# Fix the 2 bugs in this script.

import time


def tail_file(filepath, poll_interval=0.5):
    with open(filepath, "r") as f:
        f.seek(2, 0)

        while True:
            line = f.readline()
            if line:
                yield line.rstrip("\n")


def collect_new_lines(filepath, write_lines, wait=0.2):
    import threading
    collected = []

    def tail_worker():
        gen = tail_file(filepath, poll_interval=0.05)
        for _ in range(len(write_lines)):
            collected.append(next(gen))

    t = threading.Thread(target=tail_worker)
    t.start()
    time.sleep(0.05)

    with open(filepath, "a") as f:
        for line in write_lines:
            f.write(line + "\n")
            f.flush()
            time.sleep(0.02)

    t.join(timeout=3)
    return collected


if __name__ == "__main__":
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".log", delete=False) as f:
        path = f.name
        f.write("existing line\n")

    print(f"Tailing {path} - write to it to see output (Ctrl+C to stop)")
    for line in tail_file(path):
        print(f">> {line}")
