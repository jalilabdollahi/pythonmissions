# Mission 159 - Probe Runner (solution)
# Run probe snippets in a child interpreter and report whether they passed.
import subprocess
import sys


def run_probe(code):
    result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    return {
        "ok": result.returncode == 0,
        "code": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def gate(probes):
    failed = []
    for name, code in probes.items():
        if not run_probe(code)["ok"]:
            failed.append(name)
    return failed
