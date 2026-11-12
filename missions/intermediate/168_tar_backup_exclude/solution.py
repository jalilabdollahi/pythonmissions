# Mission 168 - Tidy Tarball (solution)
# Create a gzip tar backup of a directory with exclusion patterns.
import fnmatch
import os
import tarfile


def relname(path, src):
    return os.path.relpath(path, src).replace(os.sep, "/")


def is_excluded(rel, patterns):
    name = rel.rsplit("/", 1)[-1]
    return any(fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(rel, pattern) for pattern in patterns)


def make_backup(src, archive_path, exclude=()):
    src = os.path.abspath(src)
    added = 0
    with tarfile.open(archive_path, "w:gz") as tar:
        for dirpath, dirnames, filenames in os.walk(src):
            dirnames[:] = [
                d for d in dirnames
                if not is_excluded(relname(os.path.join(dirpath, d), src), exclude)
            ]
            for name in sorted(filenames):
                full = os.path.join(dirpath, name)
                rel = relname(full, src)
                if is_excluded(rel, exclude):
                    continue
                tar.add(full, arcname=rel, recursive=False)
                added += 1
    return added


def list_backup(archive_path):
    with tarfile.open(archive_path, "r:gz") as tar:
        return sorted(m.name for m in tar.getmembers() if m.isfile())
