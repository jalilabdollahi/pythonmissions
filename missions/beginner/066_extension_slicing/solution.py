# Mission 066 - Four-Letter Extensions (solution)
# Groups build outputs by file extension for upload.
from pathlib import Path


def extension(filename):
    return Path(filename).suffix.lstrip(".").lower()


def group_by_extension(names):
    groups = {}
    for name in names:
        groups.setdefault(extension(name), []).append(name)
    return {ext: sorted(items) for ext, items in groups.items()}


def count_by_extension(names):
    return {ext: len(items) for ext, items in group_by_extension(names).items()}


def upload_folder(name):
    ext = extension(name)
    return ext if ext else "misc"


def folders(names):
    return sorted({upload_folder(n) for n in names})


def stem_of(filename):
    return Path(filename).stem


if __name__ == "__main__":
    print(folders(["app.jar", "index.html", "Makefile"]))
