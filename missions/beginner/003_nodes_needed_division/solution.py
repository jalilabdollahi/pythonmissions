# Mission 003 - Node Count Shortfall (solution)
# Computes how many worker nodes a number of pods needs.
def nodes_needed(pods, pods_per_node):
    return -(-pods // pods_per_node)


def monthly_cost(pods, pods_per_node, price_per_node):
    nodes = nodes_needed(pods, pods_per_node)
    return nodes * price_per_node


def spare_slots(pods, pods_per_node):
    nodes = nodes_needed(pods, pods_per_node)
    return nodes * pods_per_node - pods


if __name__ == "__main__":
    print(nodes_needed(10, 4), monthly_cost(10, 4, 70))
