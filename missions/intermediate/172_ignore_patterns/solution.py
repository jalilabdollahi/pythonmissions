# Mission 172 - Dockerignore Duel (solution)
# Decide which paths a gitignore-style pattern list excludes from a build context.
import fnmatch


def _matches(path, pattern):
    if pattern.endswith("/"):
        directory = pattern.rstrip("/")
        return path.startswith(directory + "/") or ("/" + directory + "/") in ("/" + path)
    if "/" in pattern:
        return fnmatch.fnmatchcase(path, pattern)
    return fnmatch.fnmatchcase(path.split("/")[-1], pattern)


def is_ignored(path, patterns):
    ignored = False
    for raw in patterns:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        negate = line.startswith("!")
        if negate:
            line = line[1:]
        if _matches(path, line):
            ignored = not negate
    return ignored


def filter_paths(paths, patterns):
    return [p for p in paths if not is_ignored(p, patterns)]


def main(argv=None):
    import sys

    args = sys.argv[1:] if argv is None else argv
    rules = ["*.log", "build/", "!keep.log"]
    paths = args or ["app.py", "debug.log", "keep.log", "build/out.bin"]
    for path in paths:
        print("%-16s %s" % (path, "ignored" if is_ignored(path, rules) else "kept"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
