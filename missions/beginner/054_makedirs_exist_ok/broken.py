# Mission 054 - Second Deploy, Same Directory
# Creates per-release directories for the deploy pipeline.
from pathlib import Path


def prepare_release(base, version):
    release = Path(base) / version
    release.mkdir(exist_ok=True)
    logs = release / "logs"
    logs.mkdir(parents=True)
    return release


def list_releases(base):
    root = Path(base)
    if not root.exists():
        return []
    return sorted(p.name for p in root.iterdir() if p.is_dir())


def mark_current(base, version):
    release = prepare_release(base, version)
    marker = release / "CURRENT"
    marker.write_text(version + "\n")
    return marker


if __name__ == "__main__":
    print(prepare_release("/tmp/lumen-releases", "2024.06"))
