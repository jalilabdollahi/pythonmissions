# Mission 043 - Skip the Inactive Nodes
# Fix the bug.

def report_nodes(nodes):
    """Print active nodes, skip inactive, stop on shutdown."""
    results = []
    for node in nodes:
        if node["status"] == "inactive":
            break
        if node["status"] == "shutdown":
            continue
        results.append(node["name"])
    return results

if __name__ == "__main__":
    nodes = [
        {"name": "node-01", "status": "active"},
        {"name": "node-02", "status": "inactive"},
        {"name": "node-03", "status": "active"},
        {"name": "node-04", "status": "shutdown"},
        {"name": "node-05", "status": "active"},
    ]
    print(report_nodes(nodes))
