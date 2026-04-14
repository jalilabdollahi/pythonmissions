# Mission 021 - Solution

def merge_servers(base, new_servers):
    result = list(base)
    result.extend(new_servers)
    return result

if __name__ == "__main__":
    existing = ["web-01", "web-02"]
    scaling_up = ["web-03", "web-04"]
    print(merge_servers(existing, scaling_up))
