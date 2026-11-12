# Mission 007 - The Missing Replica (solution)
# Generates numbered replica names for a stateful service.
def replica_names(app, count):
    names = []
    for number in range(1, count + 1):
        names.append(f"{app}-{number}")
    return names


def promotion_order(app, count):
    return list(reversed(replica_names(app, count)))


if __name__ == "__main__":
    print(promotion_order("quarry-db", 5))
