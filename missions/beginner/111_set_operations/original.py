# Mission 111 - Find Common Failing Hosts
def common_failures(set_a, set_b):
    """Return hosts failing in both monitoring systems."""
    return set_a.union(set_b)

if __name__ == "__main__":
    mon1 = {"web-01", "web-02", "db-01"}
    mon2 = {"web-02", "db-01", "api-01"}
    print(common_failures(mon1, mon2))
