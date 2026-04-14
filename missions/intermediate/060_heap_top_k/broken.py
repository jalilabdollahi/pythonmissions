# Mission 060 - Top-K Error Sources
# Fix the 2 bugs in this script.
import heapq

def top_k_errors(error_counts, k):
    """Return top-k (service, count) pairs by count, descending."""
    if k <= 0 or not error_counts:
        return []
    return heapq.nsmallest(k, error_counts.items(), key=lambda x: x[1])  # BUG 1: nlargest not nsmallest

def top_error_service(error_counts):
    """Return the single service with most errors."""
    if not error_counts:
        return None
    result = top_k_errors(error_counts, 1)
    return result[1]  # BUG 2: result[0] is the tuple, result[0][0] is the service name
