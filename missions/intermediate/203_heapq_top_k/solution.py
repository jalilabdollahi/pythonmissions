# Mission 203 - Slowest Endpoints Board (solution)
# Keep the k slowest endpoints in a bounded heap and print a leaderboard.
import heapq


def average_latencies(samples):
    totals = {}
    for endpoint, ms in samples:
        total, count = totals.get(endpoint, (0, 0))
        totals[endpoint] = (total + ms, count + 1)
    return {endpoint: total / count for endpoint, (total, count) in totals.items()}


def slowest_endpoints(samples, k):
    heap = []
    for endpoint, avg in average_latencies(samples).items():
        heapq.heappush(heap, (avg, endpoint))
        if len(heap) > k:
            heapq.heappop(heap)
    return [(endpoint, abs(avg)) for avg, endpoint in sorted(heap, reverse=True)]


def worst_endpoint(samples):
    rows = slowest_endpoints(samples, 1)
    return rows[0][0] if rows else None


def breaching(samples, limit_ms):
    avgs = average_latencies(samples)
    return sorted(name for name, avg in avgs.items() if avg > limit_ms)


def format_board(rows):
    if not rows:
        return "(no data)"
    lines = []
    for rank, (endpoint, avg) in enumerate(rows, start=1):
        lines.append(f"{rank}. {endpoint:<14} {avg:8.1f} ms")
    return "\n".join(lines)


if __name__ == "__main__":
    demo = [("/login", 120), ("/search", 480), ("/search", 520), ("/health", 5)]
    print(format_board(slowest_endpoints(demo, 2)))
