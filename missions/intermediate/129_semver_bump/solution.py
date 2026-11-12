# Mission 129 - Version Bumper (solution)
# Parse, bump and compare semantic version strings.
import re

VERSION_RE = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?(?:\+.*)?$")


def parse(version):
    match = VERSION_RE.match(version.strip())
    if match is None:
        raise ValueError(f"not a semantic version: {version!r}")
    major, minor, patch, pre = match.groups()
    return int(major), int(minor), int(patch), pre


def bump(version, part):
    major, minor, patch, _ = parse(version)
    if part == "major":
        major, minor, patch = major + 1, 0, 0
    elif part == "minor":
        minor, patch = minor + 1, 0
    elif part == "patch":
        patch += 1
    else:
        raise ValueError(f"unknown part: {part}")
    return f"{major}.{minor}.{patch}"


def sort_key(version):
    major, minor, patch, pre = parse(version)
    return (major, minor, patch, pre is None)


def latest(versions):
    if not versions:
        raise ValueError("no versions given")
    return max(versions, key=sort_key)
