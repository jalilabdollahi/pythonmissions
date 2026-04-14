# Mission 058 - Binary Search
# Fix the 2 bugs in this script.

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return left  # BUG 1: should return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def find_log_entry(logs, timestamp):
    """logs is list of (timestamp, message) tuples, sorted by timestamp."""
    timestamps = [t for t, _ in logs]
    idx = binary_search(timestamps, timestamp)
    if idx == -1:
        return None
    return logs[idx][1]

def count_in_range(arr, lo, hi):
    """Count elements in sorted arr between lo and hi inclusive."""
    left_idx = binary_search(arr, lo)
    right_idx = binary_search(arr, hi)
    if left_idx == -1 or right_idx == -1:
        return 0
    return right_idx - left_idx  # BUG 2: should be right_idx - left_idx + 1
