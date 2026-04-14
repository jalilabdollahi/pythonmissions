# Mission 052 - Solution
def sort_by_cpu(servers):
    return sorted(servers, key=lambda s: s["cpu_pct"])

if __name__ == "__main__":
    svrs = [{"name":"web-01","cpu_pct":75},{"name":"api-01","cpu_pct":20},{"name":"db-01","cpu_pct":90}]
    for s in sort_by_cpu(svrs):
        print(s)
