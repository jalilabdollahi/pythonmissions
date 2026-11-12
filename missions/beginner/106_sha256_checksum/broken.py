# Mission 106 - Artifact Fingerprint
# Computes a SHA-256 fingerprint of a build artifact file.
import hashlib

CHUNK_SIZE = 8192


def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "r") as handle:
        while True:
            chunk = handle.read(CHUNK_SIZE)
            if not chunk:
                break
            h.update(chunk)
    return h.digest()


def verify_checksum(path, expected):
    return file_sha256(path) == expected.strip().lower()


def describe(path):
    return f"{path}  sha256:{file_sha256(path)}"


if __name__ == "__main__":
    import sys

    for name in sys.argv[1:]:
        print(describe(name))
