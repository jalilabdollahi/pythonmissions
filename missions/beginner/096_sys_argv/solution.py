# Mission 096 - Solution
import sys

def get_env_arg(argv=None):
    if argv is None:
        argv = sys.argv
    return argv[1]

if __name__ == "__main__":
    print(get_env_arg())
