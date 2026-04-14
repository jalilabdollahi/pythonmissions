# Mission 140 - Solution
def disk_delta(before_mb, after_mb):
    return abs(after_mb - before_mb)

if __name__ == "__main__":
    print(disk_delta(500, 480))
    print(disk_delta(480, 500))
