# Mission 135 - Build the Deploy Script
def build_script(commands):
    """Join commands with newlines to form a shell script."""
    return " ".join(commands)

if __name__ == "__main__":
    cmds = ["#!/bin/bash", "set -e", "docker pull myapp:latest", "docker restart myapp"]
    print(build_script(cmds))
