# Mission 096 - Parse the Script Argument
import sys

def get_env_arg(argv=None):
    """Return the first CLI argument (environment name)."""
    if argv is None:
        argv = sys.argv
    return argv[0]

if __name__ == "__main__":
    print(get_env_arg())
