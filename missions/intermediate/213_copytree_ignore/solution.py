# Mission 213 - Release Staging Copy (solution)
# Stage a source tree for packaging, skipping build junk.
import shutil
from pathlib import Path

IGNORED = ["__pycache__", ".git", "*.pyc", "*.log"]


def manifest(root):
    root = Path(root)
    return sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file())


def stage_release(src, dst, extra_ignore=()):
    patterns = shutil.ignore_patterns(*IGNORED, *extra_ignore)
    shutil.copytree(src, dst, ignore=patterns, dirs_exist_ok=True)
    return manifest(dst)


def is_clean(dst):
    dst = Path(dst)
    for pattern in ("*.pyc", "*.log"):
        if any(dst.rglob(pattern)):
            return False
    return not any(p.name in ("__pycache__", ".git") for p in dst.rglob("*"))


def skipped(src, dst):
    kept = set(manifest(dst))
    return [name for name in manifest(src) if name not in kept]


def by_extension(dst):
    counts = {}
    for name in manifest(dst):
        suffix = Path(name).suffix or "(none)"
        counts[suffix] = counts.get(suffix, 0) + 1
    return counts


def total_size(dst):
    return sum(p.stat().st_size for p in Path(dst).rglob("*") if p.is_file())


if __name__ == "__main__":
    print(stage_release("src", "stage"))
