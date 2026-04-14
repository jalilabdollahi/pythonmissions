# Mission 043 - Solution

def report_nodes(nodes):
    results = []
    for node in nodes:
        if node["status"] == "inactive":
            continue
        if node["status"] == "shutdown":
            break
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
