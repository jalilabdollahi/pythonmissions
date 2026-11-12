# Mission 016 - Percent Without The Percent
# Formats storage pool fill levels as percentages.
def fill_label(used, total):
    return f"{used / total:.1}"


def pool_line(name, used, total):
    return f"{name}: {fill_label(used, total)}"


def report(pools):
    return [pool_line(name, used, total) for name, (used, total) in sorted(pools.items())]


if __name__ == "__main__":
    for line in report({"ssd-a": (7, 8), "hdd-b": (1, 3)}):
        print(line)
