# Mission 024 - Solution

def remove_if_present(pool, server):
    if server in pool:
        pool.remove(server)

if __name__ == "__main__":
    active = ["web-01", "web-02", "web-03"]
    remove_if_present(active, "web-02")
    remove_if_present(active, "web-99")
    print(active)
