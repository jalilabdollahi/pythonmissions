# Mission 135 - Solution
def build_script(commands):
    return "\n".join(commands)

if __name__ == "__main__":
    cmds = ["#!/bin/bash", "set -e", "docker pull myapp:latest", "docker restart myapp"]
    print(build_script(cmds))
