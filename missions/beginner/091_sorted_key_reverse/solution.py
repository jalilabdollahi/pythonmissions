# Mission 091 - Solution
def top_cpu(servers):
    return sorted(servers, key=lambda s: s["cpu_pct"], reverse=True)

if __name__ == "__main__":
    svrs = [{"name":"web-01","cpu_pct":45},{"name":"db-01","cpu_pct":92},{"name":"api-01","cpu_pct":60}]
    for s in top_cpu(svrs):
        print(s)
