# Mission 163 - Ghost Daemon
# Pidfile handling for a single-instance background worker.
import os


class AlreadyRunning(Exception):
    pass


def read_pid(path):
    try:
        with open(path) as handle:
            return int(handle.read().strip())
    except FileNotFoundError:
        return None


def status(path, is_alive):
    pid = read_pid(path)
    if pid is None:
        return "stopped"
    return "running" if is_alive(pid) else "stale"


def acquire(path, pid, is_alive):
    existing = read_pid(path)
    if existing is not None:
        raise AlreadyRunning(f"daemon already running with pid {existing}")
    with open(path, "w") as handle:
        handle.write(str(pid))


def release(path, pid):
    if os.path.exists(path):
        os.remove(path)
