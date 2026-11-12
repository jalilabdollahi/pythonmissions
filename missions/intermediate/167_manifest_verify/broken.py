# Mission 167 - Checksum Audit
# Verify files against a SHA256SUMS style manifest.
import hashlib
import os


def file_digest(path, chunk_size=65536):
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest = hashlib.sha256()
            digest.update(chunk)
    return digest.hexdigest()


def parse_manifest(text):
    entries = []
    for line in text.splitlines():
        if not line.strip():
            continue
        expected, name = line.split(None, 1)
        entries.append((expected, name.strip()))
    return entries


def verify_manifest(root, manifest_text, chunk_size=65536):
    report = {"ok": [], "mismatch": [], "missing": []}
    for expected, name in parse_manifest(manifest_text):
        actual = file_digest(os.path.join(root, name), chunk_size)
        bucket = "ok" if actual == expected else "mismatch"
        report[bucket].append(name)
    return report
