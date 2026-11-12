# Mission 051 - Glued Paths At Orbit Freight
# Builds filesystem locations for release artifacts.
from pathlib import Path

ARTIFACT_ROOT = "/srv/releases"


def release_dir(project, version, root=ARTIFACT_ROOT):
    return Path(root + project) / version


def artifact_path(project, version, filename, root=ARTIFACT_ROOT):
    return release_dir(project, version, root) / filename


def checksum_path(project, version, filename, root=ARTIFACT_ROOT):
    artifact = artifact_path(project, version, filename, root)
    return artifact.with_name(artifact.name + ".sha256")


def latest_link(project, root=ARTIFACT_ROOT):
    return Path(root + project) / "latest"


def all_paths(project, version, filename, root=ARTIFACT_ROOT):
    return [
        artifact_path(project, version, filename, root),
        checksum_path(project, version, filename, root),
        latest_link(project, root),
    ]


if __name__ == "__main__":
    for p in all_paths("billing", "1.4.2", "billing.tar.gz"):
        print(p)
