# Mission 140 - Calculate Disk Delta
def disk_delta(before_mb, after_mb):
    """Return absolute change in disk free space (MB)."""
    return after_mb - before_mb

if __name__ == "__main__":
    print(disk_delta(500, 480))
    print(disk_delta(480, 500))
