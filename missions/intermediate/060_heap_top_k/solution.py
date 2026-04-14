# Mission 060 - Top-K Error Sources
# Fixed solution
import heapq

def top_k_errors(error_counts, k):
    if k <= 0 or not error_counts:
        return []
    return heapq.nlargest(k, error_counts.items(), key=lambda x: x[1])

def top_error_service(error_counts):
    if not error_counts:
        return None
    result = top_k_errors(error_counts, 1)
    return result[0][0]
