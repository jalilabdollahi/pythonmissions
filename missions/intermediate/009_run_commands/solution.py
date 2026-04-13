# Mission 09 - Solution

import shlex
import subprocess


def run_command(command):
    if isinstance(command, str):
        args = shlex.split(command)
    else:
        args = command

    result = subprocess.run(args, capture_output=True)

    output = result.stdout.decode("utf-8")
    return output, result.returncode


def run_and_check(command):
    output, returncode = run_command(command)
    if returncode != 0:
        raise RuntimeError(f"Command failed (exit {returncode}): {command}")
    return output


def get_disk_usage(path="/"):
    output, _ = run_command(f"df -h {path}")
    return output


if __name__ == "__main__":
    output, code = run_command("echo hello from subprocess")
    print(f"Output: {output!r}")
    print(f"Return code: {code}")
