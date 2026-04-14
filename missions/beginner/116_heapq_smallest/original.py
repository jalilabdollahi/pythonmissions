# Mission 116 - Find the Three Slowest Endpoints
import heapq

def slowest_three(times):
    """Return the 3 largest response times."""
    return heapq.nsmallest(3, times)

if __name__ == "__main__":
    times = [120, 340, 89, 2000, 456, 1500, 78, 900]
    print(slowest_three(times))
