# Mission 038 - Solution

def build_port_map(names, ports):
    return {name: port for name, port in zip(names, ports)}

if __name__ == "__main__":
    names = ["web", "api", "db"]
    ports = [80, 8080, 5432]
    print(build_port_map(names, ports))
