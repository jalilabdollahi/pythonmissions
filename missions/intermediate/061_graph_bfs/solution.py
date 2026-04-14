# Mission 061 - Graph BFS
# Fixed solution
from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    result = []
    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        result.append(node)
        queue.extend(graph.get(node, []))
    return result

def find_path(graph, start, end):
    reachable = bfs(graph, start)
    return end in reachable
