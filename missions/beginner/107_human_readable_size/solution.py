# Mission 107 - Disk Report Units (solution)
# Converts byte counts into KiB, MiB and GiB for a storage report.
UNITS = ["B", "KiB", "MiB", "GiB", "TiB"]


def human_size(n):
    if n < 0:
        raise ValueError("size cannot be negative")
    size = float(n)
    unit = 0
    while size >= 1024 and unit < len(UNITS) - 1:
        size /= 1024
        unit += 1
    if unit == 0:
        return f"{int(size)} B"
    return f"{size:.1f} {UNITS[unit]}"


def largest_volume(volumes):
    name = max(volumes, key=volumes.get)
    return f"{name}: {human_size(volumes[name])}"


def total_size(volumes):
    return human_size(sum(volumes.values()))


if __name__ == "__main__":
    data = {"media-archive": 5 * 1024 ** 3, "logs": 1_000_000, "tmp": 512}
    print(largest_volume(data))
    print(total_size(data))
