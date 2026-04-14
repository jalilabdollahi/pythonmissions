# Mission 058 - Binary Search
# Fixed solution

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def find_log_entry(logs, timestamp):
    timestamps = [t for t, _ in logs]
    idx = binary_search(timestamps, timestamp)
    if idx == -1:
        return None
    return logs[idx][1]

def count_in_range(arr, lo, hi):
    left_idx = binary_search(arr, lo)
    right_idx = binary_search(arr, hi)
    if left_idx == -1 or right_idx == -1:
        return 0
    return right_idx - left_idx + 1
