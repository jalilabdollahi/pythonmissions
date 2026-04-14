# Mission 091 - Sort Servers by CPU Descending
def top_cpu(servers):
    """Return servers sorted by cpu_pct highest first."""
    return sorted(servers, key=lambda s: s["cpu_pct"], reverse=False)

if __name__ == "__main__":
    svrs = [{"name":"web-01","cpu_pct":45},{"name":"db-01","cpu_pct":92},{"name":"api-01","cpu_pct":60}]
    for s in top_cpu(svrs):
        print(s)
