# Mission 027 - Find the Node Index
# Fix the bug.

def get_node_index(nodes, target):
    """Return index of target in nodes, or -1 if not found."""
    return nodes.index(target)

if __name__ == "__main__":
    nodes = ["node-01", "node-02", "node-03"]
    print(get_node_index(nodes, "node-02"))
    print(get_node_index(nodes, "node-99"))
