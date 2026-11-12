# Mission 049 - Mojibake in the Changelog (solution)
# Read and write UTF-8 release notes.


def read_changelog(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def write_summary(path, entries):
    with open(path, "w", encoding="utf-8") as handle:
        for entry in entries:
            handle.write(entry + "\n")
