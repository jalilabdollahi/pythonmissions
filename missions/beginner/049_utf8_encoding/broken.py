# Mission 049 - Mojibake in the Changelog
# Read and write UTF-8 release notes.


def read_changelog(path):
    with open(path, encoding="ascii") as handle:
        return handle.read()


def write_summary(path, entries):
    with open(path, "w", encoding="latin-1") as handle:
        for entry in entries:
            handle.write(entry + "\n")
