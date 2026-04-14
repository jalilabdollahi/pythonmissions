# Mission 136 - Extract All Hostnames
def get_hostnames(endpoints):
    """Return list of hostname strings from endpoint dicts."""
    return [e["host"] for e in endpoints]

if __name__ == "__main__":
    endpoints = [
        {"hostname": "web-01.internal", "port": 80},
        {"hostname": "api-01.internal", "port": 8080},
    ]
    print(get_hostnames(endpoints))
