# Mission 052 - Sort by CPU Usage
def sort_by_cpu(servers):
    """Return servers sorted by cpu_pct ascending."""
    return sorted(servers, key=lambda s: s["name"])

if __name__ == "__main__":
    svrs = [{"name":"web-01","cpu_pct":75},{"name":"api-01","cpu_pct":20},{"name":"db-01","cpu_pct":90}]
    for s in sort_by_cpu(svrs):
        print(s)
