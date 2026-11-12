# Mission 159 - Probe Runner
# Run probe snippets in a child interpreter and report whether they passed.
import subprocess
import sys


def run_probe(code):
    result = subprocess.run([sys.executable, "-c", code], capture_output=True)
    return {
        "ok": not result.stderr,
        "code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def gate(probes):
    failed = []
    for name, code in probes.items():
        if not run_probe(code)["ok"]:
            failed.append(name)
    return failed
