# Mission 048 - Read Before Close (solution)
# Write a release manifest and verify it by reading it back.


def stage_manifest(path, content):
    with open(path, "w", encoding="utf-8") as writer:
        writer.write(content)
    with open(path, encoding="utf-8") as reader:
        stored = reader.read()
    return stored == content


def append_and_count(path, line):
    with open(path, "a", encoding="utf-8") as writer:
        writer.write(line + "\n")
    with open(path, encoding="utf-8") as reader:
        count = len(reader.read().splitlines())
    return count
