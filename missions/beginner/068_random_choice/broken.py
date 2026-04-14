# Mission 068 - Pick a Random Server
import random

def pick_server(servers):
    """Return a random server from the list."""
    return servers[random.randint(0, len(servers))]

if __name__ == "__main__":
    pool = ["web-01", "web-02", "web-03"]
    print(pick_server(pool))
