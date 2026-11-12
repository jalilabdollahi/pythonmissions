# Mission 160 - Quoting Trouble
# Call child Python processes with caller-supplied text.
import subprocess
import sys

LENGTH_SCRIPT = "import sys; print(len(sys.argv[1]))"
MANY_SCRIPT = "import sys; print(*[len(a) for a in sys.argv[1:]])"


def measure(arg):
    command = f'"{sys.executable}" -c "{LENGTH_SCRIPT}" {arg}'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return int(result.stdout.strip())


def measure_many(args):
    argv = " ".join(args).split()
    result = subprocess.run(
        [sys.executable, "-c", MANY_SCRIPT, *argv], capture_output=True, text=True
    )
    return [int(part) for part in result.stdout.split()]


def measure_inline(text):
    code = f"print(len('{text}'))"
    result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    return int(result.stdout.strip())
