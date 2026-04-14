# Mission 018 - Subprocess Runner
# Fixed solution
import subprocess

def run_command(cmd):
    """Run a shell command and return (stdout, returncode)."""
    result = subprocess.run(cmd, shell=True, capture_output=True)
    output = result.stdout.decode() if result.stdout else ""
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")
    return output, result.returncode

def get_disk_usage():
    out, _ = run_command("df -h /")
    return out
