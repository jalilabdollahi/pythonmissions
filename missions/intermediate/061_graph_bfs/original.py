# Mission 061 - Graph BFS
# Fix the 2 bugs in this script.
from collections import deque

def bfs(graph, start):
    """Return all nodes reachable from start via BFS."""
    visited = set()
    queue = deque([start])
    result = []
    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        result.append(node)
        queue = deque(graph.get(node, []))  # BUG 1: replaces queue instead of extending
    return result

def find_path(graph, start, end):
    """Find if a path exists from start to end."""
    reachable = bfs(graph, start)
    return start in reachable  # BUG 2: should check if end is reachable
