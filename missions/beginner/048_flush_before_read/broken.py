# Mission 048 - Read Before Close
# Write a release manifest and verify it by reading it back.


def stage_manifest(path, content):
    writer = open(path, "w", encoding="utf-8")
    writer.write(content)
    with open(path, encoding="utf-8") as reader:
        stored = reader.read()
    writer.close()
    return stored == content


def append_and_count(path, line):
    writer = open(path, "a", encoding="utf-8")
    writer.write(line + "\n")
    with open(path, encoding="utf-8") as reader:
        count = len(reader.read().splitlines())
    writer.close()
    return count
