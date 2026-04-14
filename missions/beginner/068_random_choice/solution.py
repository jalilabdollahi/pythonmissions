# Mission 068 - Solution
import random

def pick_server(servers):
    return random.choice(servers)

if __name__ == "__main__":
    pool = ["web-01", "web-02", "web-03"]
    print(pick_server(pool))
