# Mission 117 - Solution
import bisect

def add_threshold(thresholds, value):
    bisect.insort(thresholds, value)

if __name__ == "__main__":
    thresholds = [70, 80, 90]
    add_threshold(thresholds, 85)
    print(thresholds)
