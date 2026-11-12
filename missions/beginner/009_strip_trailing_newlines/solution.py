# Mission 009 - Invisible Newlines (solution)
# Reads an allow-list of edge hostnames from a text file.
from pathlib import Path


def load_hostnames(path):
    with open(path) as handle:
        return [line.strip() for line in handle if line.strip()]


def is_registered(host, path):
    return host in load_hostnames(path)


def unregistered(hosts, path):
    known = set(load_hostnames(path))
    return [host for host in hosts if host not in known]


if __name__ == "__main__":
    print(load_hostnames(Path("edges.txt")))
