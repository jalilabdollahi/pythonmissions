# Mission 129 - Solution
class Node:
    __slots__ = ("node_id", "value")

    def __init__(self, node_id, value):
        self.node_id = node_id
        self.value = value

if __name__ == "__main__":
    n = Node("n-001", 42)
    print(n.node_id, n.value)
