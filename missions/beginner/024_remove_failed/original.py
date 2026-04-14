# Mission 024 - Remove the Failed Server
# Fix the bug.

def remove_if_present(pool, server):
    """Remove server from pool if it exists there."""
    pool.remove(server)

if __name__ == "__main__":
    active = ["web-01", "web-02", "web-03"]
    remove_if_present(active, "web-02")
    remove_if_present(active, "web-99")  # not in pool
    print(active)
