# Mission 018 - Subprocess Runner
# Fix the 2 bugs in this script.
import subprocess

def run_command(cmd):
    """Run a shell command and return (stdout, returncode)."""
    result = subprocess.run(cmd, shell=True)  # BUG 1: no capture_output=True
    output = result.stdout.decode() if result.stdout else ""
    if result.returncode == 1:  # BUG 2: any non-zero is failure, not just 1
        raise RuntimeError(f"Command failed: {cmd}")
    return output, result.returncode

def get_disk_usage():
    out, _ = run_command("df -h /")
    return out
