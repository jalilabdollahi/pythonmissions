# Mission 167 - Checksum Audit (solution)
# Verify files against a SHA256SUMS style manifest.
import hashlib
import os


def file_digest(path, chunk_size=65536):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
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
        try:
            actual = file_digest(os.path.join(root, name), chunk_size)
        except FileNotFoundError:
            report["missing"].append(name)
            continue
        bucket = "ok" if actual == expected.lower() else "mismatch"
        report[bucket].append(name)
    return report
