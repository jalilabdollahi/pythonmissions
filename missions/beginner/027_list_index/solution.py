# Mission 027 - Solution

def get_node_index(nodes, target):
    if target in nodes:
        return nodes.index(target)
    return -1

if __name__ == "__main__":
    nodes = ["node-01", "node-02", "node-03"]
    print(get_node_index(nodes, "node-02"))
    print(get_node_index(nodes, "node-99"))
