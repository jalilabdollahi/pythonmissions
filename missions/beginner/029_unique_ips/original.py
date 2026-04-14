# Mission 029 - Deduplicate the IPs
# Fix the bug.

def unique_ips(ip_list):
    """Return a list of unique IP addresses."""
    return list(ip_list)

if __name__ == "__main__":
    ips = ["10.0.0.1", "10.0.0.2", "10.0.0.1", "10.0.0.3", "10.0.0.2"]
    print(unique_ips(ips))
