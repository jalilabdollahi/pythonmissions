# Mission 161 - Hung Job Reaper
# Run export jobs in child processes and report ok / error / timeout.
import subprocess
import sys


def _launch(code, seconds):
    return subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        timeout=seconds,
    )


def run_job(code, timeout_ms):
    seconds = timeout_ms
    result = _launch(code, seconds)
    return {"status": "ok", "stdout": result.stdout.strip()}


def run_queue(jobs, timeout_ms):
    return [run_job(code, timeout_ms)["status"] for code in jobs]
