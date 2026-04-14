# Mission 021 - Extend the Server List
# Fix the bug.

def merge_servers(base, new_servers):
    """Add all new_servers to base and return the combined list."""
    result = list(base)
    result.append(new_servers)
    return result

if __name__ == "__main__":
    existing = ["web-01", "web-02"]
    scaling_up = ["web-03", "web-04"]
    print(merge_servers(existing, scaling_up))
