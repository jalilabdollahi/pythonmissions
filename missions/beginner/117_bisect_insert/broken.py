# Mission 117 - Insert into Sorted Threshold List
import bisect

def add_threshold(thresholds, value):
    """Insert value into sorted thresholds list in correct position."""
    bisect.insort(value, thresholds)

if __name__ == "__main__":
    thresholds = [70, 80, 90]
    add_threshold(thresholds, 85)
    print(thresholds)
