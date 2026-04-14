# Mission 022 - Sort the Hosts
# Fix the bug.

def sorted_hosts(hosts):
    """Return a sorted copy of the hosts list."""
    return hosts.sort()

if __name__ == "__main__":
    servers = ["web-03", "web-01", "web-02"]
    print(sorted_hosts(servers))
