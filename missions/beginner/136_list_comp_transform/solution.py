# Mission 136 - Solution
def get_hostnames(endpoints):
    return [e["hostname"] for e in endpoints]

if __name__ == "__main__":
    endpoints = [
        {"hostname": "web-01.internal", "port": 80},
        {"hostname": "api-01.internal", "port": 8080},
    ]
    print(get_hostnames(endpoints))
