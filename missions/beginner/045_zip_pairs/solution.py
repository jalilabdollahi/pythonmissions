# Mission 045 - Solution

def pair_services(hosts, ports):
    return list(zip(hosts, ports))

if __name__ == "__main__":
    hosts = ["web-01", "api-01", "db-01"]
    ports = [80, 8080, 5432]
    print(pair_services(hosts, ports))
